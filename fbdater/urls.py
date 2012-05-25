from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('facebook.views',
       # Facebook Backend Authentication URL's        
    url(r'^facebook/login/$', 'login'),
    url(r'^facebook/authentication_callback$', 'authentication_callback'),                    
)

urlpatterns += patterns('crush',
                       
    # -- HOME PAGE --
    # guest vs. member processing done at view module
    url(r'^$', 'views.home', name='home'),
    
    url(r'^home/$', 'views.home'),
    
    url(r'^accounts/login/$', 'views.home'),
    
    # -- CRUSH SEARCH -- 
    url(r'^search/$', 'views.search'),
    
    # -- CRUSH LIST --
    url(r'^crush_list/$', 'views.crush_list'),
        
    # -- ADMIRER LIST --
    url(r'^admirer_list/$', 'views.admirer_list'),
    
    # -- NOT INTERESTED LIST --
    url(r'^not_interested_list/$', 'views.not_interested_list'),
    
    # -- ADMIRER LINEUP --
    url(r'^admirer_lineup/$', 'views.admirer_lineup'),
    
    # -- INVITE FRIENDS --
    url(r'^invite/$', 'views.invite'),
    
    # -- PROFILE --
    url(r'^my_profile/$', 'views.my_profile'),

    # -- CREDITS --
    url(r'^my_credits/$', 'views.my_credits'),
    
    # -- FAQ --
    url(r'^FAQ/$', 'views.faq'),
    
    # -- TERMS & CONDITIONS --
    url(r'^terms/$', 'views.terms'),
    
)

urlpatterns += patterns('',
    # -- ADMIN PAGE -- #
    url(r'^admin/', include(admin.site.urls)),                        
    url(r'^logout/$', 'django.contrib.auth.views.logout'),

    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

)
