from django.db import models
from django.db.models import F,Q
from django.conf import settings
from smtplib import SMTPException
import hashlib, hmac
from fbdater.utils import send_mailgun_email
from fbdater.utils_email import send_mail_crush_invite,send_mail_mf_invite
# for mail testing 
#from django.core.mail import send_mail
import datetime
import requests

class InviteEmailManager(models.Manager):
    def process(self,new_email,new_relationship,new_is_for_crush):
        try:  # make sure this email does not already exist, if it does, then don't save
            duplicate_relationship_email = self.get(email=new_email,relationship=new_relationship)
            if duplicate_relationship_email.is_for_crush!=new_is_for_crush:
                # the previous email invite was of a different type.  Assume this newer email is more accurate
                # change and save the original's type
                duplicate_relationship_email.is_for_crush=new_is_for_crush
                duplicate_relationship_email.save(update_fields=['is_for_crush'])
                duplicate_relationship_email.send()
                #duplicate_relationship_email.send() # send email right away
            else:
                # only resend if email if enough time has transpired
                transpired_time = duplicate_relationship_email.date_last_sent - datetime.datetime.now() 
                if abs(transpired_time.days) > settings.MINIMUM_INVITE_RESEND_DAYS:
                    duplicate_relationship_email.send()
                                
        except: # this email doesn't exist for the same relationship, then create it unless we have reached a cap
            invite_emails=self.filter(relationship=new_relationship,is_for_crush=new_is_for_crush).order_by('date_last_sent')
            if (new_is_for_crush==True and len(invite_emails) < settings.MAXIMUM_CRUSH_INVITE_EMAILS) or (new_is_for_crush==False and len(invite_emails) < settings.MAXIMUM_MUTUAL_FRIEND_INVITE_EMAILS):
                new_invite = self.create(email=new_email,relationship=new_relationship,is_for_crush=new_is_for_crush)
                new_invite.send()
            # for now just ignore user's request and don't send out an email - we don't want to overflood the database with random emails.
                
            #else: # user has already created a maximum number of crush emails
                # overwrite the oldest invite email
                    #oldest_invite_email=invite_emails[0]
                    #oldest_invite_email.email=new_email
                    #oldest_invite_email.save(update_fields=['email'])
                    #oldest_invite_email.send() # send email out right away
                    #return False   
        return True
            
    def delete_activated_user_emails(self,crush_user):
        # find all crush relationships where target_person=crush_user
        crush_relationships=crush_user.crush_crushrelationship_set_from_target.all()
        for relationship in crush_relationships:
            # find all emails associated with interated relationship
            emails=self.filter(relationship=relationship)
            for email in emails:
                # delete every associated email
                email.delete()
        
class InviteEmail(models.Model):

    class Meta:
        # this allows the models to be broken into separate model files
        app_label = 'crush' 
    objects = InviteEmailManager()
    
    relationship = models.ForeignKey('CrushRelationship')
    email=models.CharField(max_length=200) # is this long enough?
    date_last_sent=models.DateTimeField(blank=True,null=True,default=None)
    is_for_crush=models.BooleanField(default=True) # if false, then the email was sent to a mutual friend

    def __unicode__(self):
        if self.is_for_crush == True:
            return self.email + '(crush) : ' +  str(self.relationship) 
        else:
            return self.email + '(mutual_friend) : ' +  str(self.relationship) 

    def send(self):
        crush_user= self.relationship.target_person
        crush_full_name = crush_user.first_name + " " + crush_user.last_name
        crush_short_name = crush_user.first_name + " " + crush_user.last_name[0]
        crush_first_name = crush_user.first_name
        if self.is_for_crush:
            subject = crush_short_name + ", you have an admirer!"
            send_mail_crush_invite(self.relationship.friendship_type,crush_full_name,crush_short_name,crush_first_name,self.email)

        else:
            subject = 'Your friend, ' + crush_short_name + ', has an admirer!'
            send_mail_mf_invite(crush_full_name,crush_short_name,crush_first_name,self.email)

        #send_mailgun_email("Flirtally <notifications@flirtally.com>",self.email,subject,message)
 
class Purchase(models.Model):

    class Meta:
        # this allows the models to be broken into separate model files
        app_label = 'crush' 
        
    credit_total = models.IntegerField(default=0) # e.g. 100
    price = models.DecimalField( decimal_places=2, max_digits=7 )
    purchaser = models.ForeignKey('FacebookUser')
    purchased_at = models.DateTimeField(auto_now_add=True)
    tx = models.CharField( max_length=250,blank=True,null=True )
    
    def __unicode__(self):
        return self.purchaser.first_name + ' ' + self.purchaser.last_name + ' (' + self.purchaser.username + '): $' + str(self.price) + ' (' + str(self.credit_total) + ' credits)' 
  
    def save(self,*args, **kwargs): 
        print "purchase save overridden function called" 
        if not self.pk:
            print "creating purchase  object with new credit total: " + str(self.credit_total)
            print "SERIOUSLY CREATE THIS DAMN PURCHASE OBJECT!"
            # give the relationship a secret admirer id.  this is the unique admirer identifier that is displayed to the crush)
            # get total previous admirers (past and present) and add 1
            current_user = self.purchaser
            current_user.site_credits = F('site_credits') + self.credit_total     
            current_user.save(update_fields = ['site_credits']) 
        return super(Purchase, self).save(*args,**kwargs)