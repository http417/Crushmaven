from django.http import HttpResponse,HttpResponseNotAllowed,HttpResponseNotFound,HttpResponseForbidden
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from crush.models import CrushRelationship,PlatonicRelationship,LineupMember,FacebookUser
from crush.models.globals import g_init_dict
import datetime
import time,thread
from django.db.models import Q
from utils import graph_api_fetch
from urllib2 import HTTPError

# -- Admirer List Page --
@login_required
def admirers(request,show_lineup=None):
    print "starting view function admirers()"
    global g_init_dict
    me = request.user 

    progressing_admirer_relationships = CrushRelationship.objects.progressing_admirers(me)
    past_admirers_count = CrushRelationship.objects.past_admirers(me).count()
    
    # initialize any uninitialized relationship lineups (status = None or greater than 1): (1 means initialized and 0 means initialization is in progress)
    uninitialized_relationships = progressing_admirer_relationships.filter(Q(lineup_initialization_status=None) | Q(lineup_initialization_status__gt=1))
    print "Initializing: " + str(len(uninitialized_relationships)) + " relationships"
 
    if len(uninitialized_relationships)>0:
        # reset initialize the global variable and set the number of relationships to initialize
        g_init_dict[me.username]={}    
        g_init_dict[me.username]['initialization_count'] = len(uninitialized_relationships)    
    
        for relationship in uninitialized_relationships: 
            relationship.lineup_initialization_status=0
            relationship.save(update_fields=['lineup_initialization_status'])
            print "starting lineup"
            #LineupMember.objects.initialize_lineup(relationship)
            thread.start_new_thread(LineupMember.objects.initialize_lineup,(relationship,))
            
    return render(request,'admirers.html',
                              {'profile': me.get_profile, 
                               'admirer_type': 0, # 0 is in progress, 1 completed
                               'admirer_relationships':progressing_admirer_relationships,
                               'past_admirers_count': past_admirers_count,
                               'show_lineup': show_lineup,
                               'fof_fail_status':settings.LINEUP_STATUS_CHOICES[5],
                               'minimum_lineup_members':settings.MINIMUM_LINEUP_MEMBERS,
                               'ideal_lineup_members':settings.IDEAL_LINEUP_MEMBERS,                               
                               })    
    
@login_required
def ajax_display_lineup_block(request, display_id):
    global g_init_dict
    int_display_id=int(display_id)
    print "ajax initialize lineup with display id: " + str(int_display_id)
    ajax_response = ""
    try:    
        relationship = CrushRelationship.objects.all_admirers(request.user).get(admirer_display_id=int_display_id)
    except CrushRelationship.DoesNotExist:
        ajax_response += '* ' + settings.LINEUP_STATUS_CHOICES[4] + '<button id="initialize_lineup_btn">Re-initialize</button>'
        return HttpResponse(ajax_response)
    
    crush_id = relationship.target_person.username
    rel_id_state=str(relationship.id) + '_initialization_state'
    # wait for a certain amount of time before returning a response
    counter = 0
    while True: # this loop handles condition where user is annoyingly refreshing the admirer page while the initialization is in progress     
        #print "rel_id: " + str(relationship.id) + " counter: " + str(counter) + " initialization status: " + str(relationship.lineup_initialization_status)
        
        if not crush_id in g_init_dict or g_init_dict[crush_id][rel_id_state]==2: # initialization was either a success or failed
            break
        elif counter>=settings.INITIALIZATION_TIMEOUT: # if 25 seconds have passed then give up
            print "giving up on admirer:" + str(display_id)
            relationship.lineup_initialization_status = 5
            relationship.save(update_fields=['lineup_initialization_status'])
            break
        time.sleep(1) # wait a second
        counter+=1
        
    # refetch the relationship to get updated initialization status
    try:    
        relationship = CrushRelationship.objects.all_admirers(request.user).get(admirer_display_id=int_display_id)
    except CrushRelationship.DoesNotExist:
        ajax_response += '* ' + settings.LINEUP_STATUS_CHOICES[4] + '<button id="initialize_lineup_btn">Re-initialize</button>'
        return HttpResponse(ajax_response)

    if relationship.lineup_initialization_status > 3: # for data fetching errors show a button that allows user to restart the initialization 
        ajax_response += '* ' + settings.LINEUP_STATUS_CHOICES[relationship.lineup_initialization_status] + ' <button id="initialize_lineup_btn" display_id="' + display_id + '">Re-initialize</button>'
        return HttpResponse(ajax_response)
    if relationship.lineup_initialization_status > 1: # show error message
        ajax_response += '* ' + settings.LINEUP_STATUS_CHOICES[relationship.lineup_initialization_status]
        return HttpResponse(ajax_response)

    return render(request,'lineup_block.html', {'relationship':relationship,
                                                'fail_status_5':settings.LINEUP_STATUS_CHOICES[5],
                                                'fail_status_2':settings.LINEUP_STATUS_CHOICES[2],
                                                'fail_status_3':settings.LINEUP_STATUS_CHOICES[3],})

# called if client-sided call to ajax_display_lineup_block timesout or fails for some odd reason.
@login_required
def ajax_initialization_failed(request, display_id):
    int_display_id=int(display_id)
    try:    
        relationship = CrushRelationship.objects.all_admirers(request.user).get(admirer_display_id=int_display_id)    
    except CrushRelationship.DoesNotExist:
        return HttpResponseNotFound("")
    if relationship.lineup_initialization_status == None or relationship.lineup_initialization_status == 0:
        relationship.lineup_initialization_status = 5
        relationship.save(update_fields=['lineup_initialization_status'])
    return HttpResponse("")
    
    

# -- Single Lineup (Ajax Content) Page --
@login_required
def ajax_show_lineup_slider(request,admirer_id):
    me = request.user
    try:
        admirer_rel = CrushRelationship.objects.all_admirers(me).get(admirer_display_id=admirer_id)
    except CrushRelationship.DoesNotExist:
        return HttpResponse("Error: Could not find an admirer relationship for the lineup.")

    member_set = admirer_rel.lineupmember_set.all()
    
    # need to cleanse the lineup members each time the lineup is run 
    # reason: while lineup is not complete, user may have added one of the lineup member as either a crush or a platonic frined
        
    return render(request,'lineup.html',
                              {
                               'admirer_rel':admirer_rel,
                               'member_set': member_set,
                               'number_completed_members': len(member_set.exclude(decision = None)),
                               'rating1': settings.PLATONIC_RATINGS[1],
                               'rating2': settings.PLATONIC_RATINGS[2],
                               'rating3': settings.PLATONIC_RATINGS[3],
                               'rating4': settings.PLATONIC_RATINGS[4],
                               'rating5': settings.PLATONIC_RATINGS[5],
                               })

# called by lineup lightbox slider to show an individual lineup member - and allow user to rate them
@login_required
#@csrf_exempt
def ajax_get_lineup_slide(request, display_id,lineup_position):
    print "ajax get admirer: " + str(display_id) + " lineup position: " + lineup_position
    print "please change!"
    ajax_response = ""
    me=request.user
    # obtain the admirer relationship
    try:
        admirer_rel=CrushRelationship.objects.all_admirers(me).get(admirer_display_id=display_id)
        # if lineup is not paid for, then don't show any content beyond slide 2
        if admirer_rel.is_lineup_paid == False and int(lineup_position) > 1:
        #     print "lineup_position just before forbidden error: " + lineup_position
            return HttpResponseForbidden("Error: You cannot access this content until the lineup is paid for.")
    except CrushRelationship.DoesNotExist:
        print "Error: Could not find the admirer relationship."
        return HttpResponseNotFound("Error: Could not find the admirer relationship.")
    # obtain the actual user:
    lineup_member = admirer_rel.lineupmember_set.get(position=lineup_position)
    # find or create a new user for the lineup member
    lineup_member_user=FacebookUser.objects.find_or_create_user(lineup_member.username, me.access_token, False, fb_profile=None)
    if lineup_member.user==None:
        lineup_member.user=lineup_member_user
        lineup_member.save(update_fields=['user'])
    lineup_count = len(admirer_rel.lineupmember_set.all())
    display_position=int(lineup_position) + 1;
    
    # build the basic elements
    # 1) name, photo, position info 
    ajax_response += '<div class="slide_container">'
    ajax_response +='<span class="lineup_name">' + lineup_member_user.first_name + ' ' + lineup_member_user.last_name + '</span>'#<span class="lineup_position_info">(' + str(display_position)  + ' of ' + str(lineup_count) + ')</span></span>'
    ajax_response +='<span class="lineup_mugshot"><img src="' + lineup_member_user.get_facebook_pic(125) + '"></span>'
    ajax_response +='<span class="lineup_facebook_link"><a href="http://www.facebook.com/' + lineup_member_user.username + '" target="_blank">view facebook profile<span class="view_facebook_icon"></span></a></span>'

    # if the relationship is friend-of-friend, then show pictures of mutual friends:
    if admirer_rel.friendship_type==1:
        
        try:
            friend_profile=graph_api_fetch(request.user.access_token,request.user.username + '/mutualfriends/' + lineup_member.username)
            friend=friend_profile[0]
            ajax_response +='<div id="mutual_friends">Connected through: '
            ajax_response += '<img src="http://graph.facebook.com/' + friend['id'] + '/picture?width=25&height=25" title="' + friend['name'] + '" style="height:25px;width:25px;">'
            ajax_response += '</div>'
        except HTTPError as e:
            if e.code==400: # user's access token is invalid, so force user to log back in
                return HttpResponseNotAllowed('HTTPError')
            # no need to handle any other cases i.e. timeout since this isn't a vital function
        except:
            pass
    
    ajax_response +='<div id="loading"></div><span class="lineup_decision" username="' + lineup_member_user.username + '" style="margin-top:5px">'
    
    # check to see if there is an existing crush relationship or platonic relationship:
    if lineup_member_user in me.crush_targets.all():
        ajax_response += "<span id='choice' class='crush existing_choice'>You already added " + lineup_member_user.first_name + " " + lineup_member_user.last_name + " as an attraction.</span>"
        lineup_member.decision = 0
        lineup_member.save(update_fields=['decision'])
    elif lineup_member in me.just_friends_targets.all():
        ajax_response = "<span id='choice class='platonic existing_choice'>You previously decided - Not Interested</span>"
        lineup_member.decision= 1
        lineup_member.save(update_fields=['decision'])
    else:    
        if lineup_member.decision == None:
            ajax_response += '<a href="#" class="decision button lineup_decision_button" add_type="crush" username="' + lineup_member_user.username + '" name="' + lineup_member_user.first_name + ' ' + lineup_member_user.last_name + '" member_gender= "' + lineup_member_user.gender + '" lineup_position="' + lineup_position +  '">Add as Attraction</a>' 
            ajax_response += '<br><a href="#" class="decision button lineup_decision_button" add_type="platonic" username="' + lineup_member_user.username + '" name="' + lineup_member_user.first_name + ' ' + lineup_member_user.last_name + '" member_gender= "' + lineup_member_user.gender + '" lineup_position="' + lineup_position + '">Not Interested</a>'        
       
        elif lineup_member.decision == 0:
            ajax_response += '<div class="crush choice" >"You added' + lineup_member_user.first_name + ' ' + lineup_member_user.last_name + ' as an attraction!</div>'
        else:
            ajax_response += '<div class="platonic choice">You are Not Interested in ' + lineup_member_user.first_name + ' ' + lineup_member_user.last_name + '</div>'   
    ajax_response += '</span>' # close off decision holder and decision tag
    ajax_response += '</div>' # close off slide_container
    #2) facebook button 
    #3) crush button 
    #4) platonic friend button  #
        
    return HttpResponse(ajax_response)

@login_required
def ajax_add_lineup_member(request,add_type,admirer_display_id,facebook_id,rating=3):
    print "adding member to a list"
    me=request.user
    # called from lineup.html to add a member to either the crush list or the platonic friend list
    try:
        target_user=FacebookUser.objects.get(username=facebook_id)
        try:
            admirer_rel=CrushRelationship.objects.all_admirers(me).get(admirer_display_id=admirer_display_id)
        except CrushRelationship.DoesNotExist:
            return HttpResponse("Server Error: Could not add given lineup user")
        try:
            lineup_member=admirer_rel.lineupmember_set.get(username=target_user.username)
        except LineupMember.DoesNotExist:
            print "could not find lineup member"
            return HttpResponse("Server Error: Could not add given lineup user")

        if lineup_member.decision!=None:
            # something is wrong, this person was already decided upon, so just return an error message
            # check to see if they haven't already been added as a crush
            if lineup_member.decision == 0:
                ajax_response = "<span id=\"choice\" class='crush existing_choice'>You already added " + target_user.first_name + " " + target_user.last_name + " as a an attraction.</span>"
            else:
                ajax_response = "<span id=\"choice\" class='platonic existing_choice'>You previously decided - Not Interested</span>"
            return HttpResponse(ajax_response)
        if add_type=='crush':
            CrushRelationship.objects.create(source_person=request.user, target_person=target_user)
            ajax_response = '<span class="choice crush">Added as Attraction</span>'
            lineup_member.decision=0
        else:
            PlatonicRelationship.objects.create(source_person=request.user, target_person=target_user,rating=rating)
            ajax_response = '<span class="choice platonic">Not Interested</span>'
            lineup_member.decision=1
        lineup_member.save(update_fields=['decision'])
        if len(admirer_rel.lineupmember_set.filter(decision=None)) == 0:
            admirer_rel.date_lineup_finished= datetime.datetime.now()
            admirer_rel.save(update_fields=['date_lineup_finished'])
    except FacebookUser.DoesNotExist:
        print "failed to add lineup member: " + facebook_id
        return HttpResponse("Server Error: Could not add given lineup user")  
    return HttpResponse(ajax_response)

@login_required
def ajax_update_num_platonic_friends(request):

    ajax_response = str(request.user.just_friends_targets.all().count())
    return HttpResponse(ajax_response)
@login_required
def ajax_update_num_crushes_in_progress(request):
    ajax_response = str(request.user.crush_targets.all().count())
    return HttpResponse(ajax_response)

# called when a crush response is paid for
@login_required
def ajax_update_num_new_responses(request):
    ajax_response = str(CrushRelationship.objects.visible_responded_crushes(request.user).count())
    return HttpResponse(ajax_response)

# called when a lineup goes past the payment stage
@login_required
def ajax_update_num_new_admirers(request):
    ajax_response = str(CrushRelationship.objects.new_admirers(request.user).count())
    return HttpResponse(ajax_response)

# -- Past Admirers Page --
@login_required
def admirers_past(request):
    me = request.user 
   
    admirer_completed_relationships = CrushRelationship.objects.past_admirers(me).order_by('date_added')
    progressing_admirers_count = CrushRelationship.objects.progressing_admirers(me).count()

    return render(request,'admirers.html',
                              {
                               'admirer_type': 1, # 0 is in progress, 1 completed
                               'admirer_relationships':admirer_completed_relationships,
                               'progressing_admirers_count': progressing_admirers_count,
                               'fof_fail_status':settings.LINEUP_STATUS_CHOICES[2],
                               'minimum_lineup_members':settings.MINIMUM_LINEUP_MEMBERS,
                               'ideal_lineup_members':settings.IDEAL_LINEUP_MEMBERS,  
                               })    
