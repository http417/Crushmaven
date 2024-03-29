# Django settings for fbdater project.
import os, sys

# this will set the project path to /fbdater 
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, PROJECT_PATH)
#ALLOWED_HOSTS = ['www.crushmaven.com']#new for django 1.5 
ALLOWED_HOSTS=['*']

DEBUG = False
TEMPLATE_DEBUG = DEBUG
import logging

logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s %(levelname)s %(message)s',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.db.backends': {
            'handlers': ['null'],  # Quiet by default!
            'propagate': False,
            'level':'DEBUG',
            },
    }
}

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# for testing I am running a temporary python "dumb" SMTP server that receives emails locally and displays them to the terminal
EMAIL_BACKEND = 'crush.email_backend.DKIMBackend'
DKIM_SELECTOR ='selector' 
DKIM_DOMAIN ='crushmaven.com'
DKIM_PRIVATE_KEY ='MIICXAIBAAKBgQCruqWs8uHYBt9YgidoHnfpWrdLOPYJef4p61oJhRQbuZZ3fUU/\
9iv9cs8UA/fAAphw7tnc4LO/TK5zl19Zc5IeC5gPKwETY+5b0KPSjTeV1D+ww0b2\
V1UykJ94s9MAT1QoS9e0aG5wjAgbDOV6IGccKxstL4y/pb1NMqFVdDEHDwIDAQAB\
AoGAG1qMn0LE1IsrskZxDnWj9gicH6BAGHxVDspNOiz3af8ix3+tsyV8Fk/eSjrj\
kLMZIwv4qeUk3HjTZNgcuPveryWYd0Ed8JWfgh8ZFOYv9yec/KH6dcIJ67AorflU\
ySs7UhBw6Z90GMo9Flgp6fk7kQ348nYsvZ8chAkmcOTDbskCQQDc7JTH6yd8gfZ9\
POcESMY+GVoOht4hxU76CNyDiDaF9cn8AYN75p6jAIAG/YeVo04FG7sEne11220F\
OaeMqyVLAkEAxv6K5svRrLZKiAY5aijGnwxcw6JBiyHVqC/nG4COStcdTl2oLCBs\
Wb4LpyptU8UlooDSJj50HmsUpCK+LtQ+zQJBAIljRxMcli3D1LoFidUMPNyZf3vR\
O4rc3UR5Bkl2CBI+zCG//ziqLrVHtlaijBLuv7JFkIRKgkXs81twg1XjiQkCQAcV\
dqJirRMl5h9TgWW7D98HlKHOO+EVEkMLeYGsIOSfJcbtZJg1i0Xikw2fYAb0ZLOV\
PGXqIT4X98MkDXsjSR0CQB3fGWb111MJEMQnioFqmfWFXRbZ4JRCPnc+aXOefvaX\
ZNxvVb+fGonCdYMOiK8aYbstvqe2YuRydGTWGfR8ymo='
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_NOTIFICATION_USER','')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_NOTIFICATION_PASSWORD','')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT,'../media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#STATIC_ROOT = 'staticfiles'
#STATIC_URL = '/static/'

#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, 'static'),
#)

STATIC_ROOT = os.path.join(SITE_ROOT,'../staticfiles')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# HEROKU ADD-ON SUMO CDN:
# had lots of problems concatenating environment variable with strings!!!! this finally worked
#CDN_URL = os.getenv('CDN_SUMO_URL')
#STATIC_URL = 'http://' + str(CDN_URL) + '/static/'



# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

LOGIN_URL = '/home/' #where to direct user if they try to access a page where login required

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2di)!u)^iayw+r%theflbuyve&amp;rb4n*407rum9&amp;#&amp;=1p3vsko4'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',                           
    'django.core.context_processors.request',
    'django.core.context_processors.csrf',
    'django.core.context_processors.static',
    'crush.context_processor.context_processor',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
   # 'crush.ssl.SSLRedirect',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'fbdater.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'fbdater.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    
    # MAC PATH:
    #os.path.join(PROJECT_PATH, 'templates'), 
    # PC PATCH:
    os.path.join(SITE_ROOT, '../templates'), 
    
    
    #"templates"
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'facebook',
    'crush',
    'postman',
    'ajax_select',
    'south',
)

# using heroku MEMCACHIER ADD-ON
os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';')
os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

CACHES = {
  'default': {
    'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
    'TIMEOUT': 160000, #86,000 seconds is about one day so expire the cookie in 2 days
    'BINARY': True,
    'OPTIONS': { 'tcp_nodelay': True }
  }
}
# old cache for local memory - will not likely work on Heroku because a dyno may be dynamically run on separate instances - which would invalidate cache
#CACHES={
#        'default' : {
#          'BACKEND':'django.core.cache.backends.locmem.LocMemCache',         
#                     }
#        }

INACTIVE_USER_CACHE_KEY = 'all_inactive_user_list'
INVITE_INACTIVE_USER_CACHE_KEY = "all_invite_inactive_user_list"
FB_FETCH_COOKIE = 'fb_fetch_cookie'
DATE_NOTIFICATIONS_LAST_SENT_CACHE_KEY = 'date_notifiactions_last_sent'

# define the custom user that inherits from Django's User model
AUTH_USER_MODEL = 'crush.FacebookUser'


# Facebook settings are set via environment variables
FACEBOOK_APP_ID = '563185300424922' # CrushMaven App on Facebook
FACEBOOK_APP_SECRET = '4a0d7982f553640cbb2c4dde20d6e2b8'
FACEBOOK_APP_TOKEN='563185300424922|z-qnM1SxXECt41nuRTmGuCLcIJI'
#FACEBOOK_SCOPE = 'user_about_me, friends_about_me, user_relationship_details, user_relationships, friends_relationships, friends_relationship_details, email,user_birthday, friends_birthday, user_location, friends_location'
FACEBOOK_SCOPE = 'user_about_me, friends_about_me, user_relationship_details, user_relationships, friends_relationships, friends_relationship_details, email'


AUTHENTICATION_BACKENDS = (
    'facebook.backend.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)

URLLIB_TIMEOUT=30
LINEUP_BLOCK_TIMEOUT=120000 # this determines how long (in millisecons) each admirer block should wait for initialization request to return a result. if timeout, then relationship initialization status set to error state (via ajax call)
INITIALIZATION_TIMEOUT=120 # maximum amt of time in seconds before ajax initialization times out
INITIALIZATION_RESTART_TIME_CRUSH_STATUS_0=4 #minutes to wait to restart initialization if the current status is 0 (progressing)
INITIALIZATION_RESTART_TIME_CRUSH_STATUS_2=12 #hours to wait to restart initialization if the current status is 2 (admirer doesn't have enough friends)
INITIALIZATION_RESTART_TIME_CRUSH_STATUS_3=15 #minutes to wait to restart initialization if the current status is 3 (crush doesn't have enough friends)
INITIALIZATION_RESTART_TIME_CRUSH_STATUS_4_5=2 #minutes to wait to restart initialization if the current status is 4 or 5 (some sort of network or bug in system)

INITIALIZATION_THREADING=True
SEND_NOTIFICATIONS=True
# auto delay the response between the start time and end time (in minutes)
CRUSH_RESPONSE_DELAY_START = 180 # 180 default = 3hours x 60 minutes =  180
CRUSH_RESPONSE_DELAY_END = 2880 # 2160 default = 48 hours x 60 minutes = 2880
CRUSH_RESPONSE_MINIMUM_AUTO_WAIT = 4320 # give original admirer at least this much time (in hours) to view response and thus auto notify original target 72 hours x 60 minutes = 4320
LINEUP_EXPIRATION_HOURS=72 # number of hours after which the lineup expires and undecided members are auto set to platonic
STARTING_CREDITS=0 # changed to 0 in production on 1/14/14
MINIMUM_LINEUP_MEMBERS=4 # change to 4 in production = this value excludes the secret admirer themself
IDEAL_LINEUP_MEMBERS=9 # change to 9 in production = this value excludes the secret admirer themself
MAXIMUM_LINEUP_FRIEND_COUNT=1100 # lineup users cannot have more than this number of friends - this is a hack to prevent users in lineups that are businesses
NUMBER_LINEUP_RECENT_FRIENDS = 4 # number of lineup friends that come from recently added friends
FRIENDS_WITH_ADMIRERS_SEARCH_DELAY=1# 0 # default is = 1 hours
MINIMUM_DELETION_DAYS_SINCE_ADD=7# 7 is default
MINIMUM_DELETION_DAYS_SINCE_RESPONSE_VIEW=7#7 is default
MAXIMUM_CRUSH_INVITE_EMAILS=7
MAXIMUM_MUTUAL_FRIEND_INVITE_EMAILS=30
MINIMUM_INVITE_RESEND_DAYS=7 # DEFAULT = 7 (days)
NUMBER_ADMIRER_FRIENDS_TO_INVITE=20 #DEFAULT=20 used to determine number of friends to ask admirer to invite
MAXIMUM_CRUSHES=50
SEND_NOTIFICATIONS=True
#PLATONIC_RATINGS = {
#                    5:'Very attractive - just not for me',
#                    4:'Somewhat attractive - just not for me', 
#                    3:"I'm indifferent",
#                    2:'Slightly unattractive',
#                    1:'Very unattractive',
#                     }
PLATONIC_RATINGS = {
                    1:'Just interested in friendship',
                    2:'Not physically attracted to ',
                    3:'Not interested in any relations w/', 
                    4:"Bad timing - I'm in a relationship",
                    5:'Other',
                     }

DELETION_ERROR = {
                  0:'To prevent users from gaming the system i.e. figuring out what your feelings are without revealing their own, crushes may only be removed once ' + str(MINIMUM_DELETION_DAYS_SINCE_ADD) + ' days have passed since they were first added.',
                  1:'Your crush is currently taking your admirer lineup.  To prevent other users from gaming the system i.e. figuring out what your feelings are without revealing their own, crushes can not be removed while the user is interacting with the associated admirer lineup.',
                  2:"To prevent users from gaming the system i.e. figuring out what your feelings are without revealing their own, crushes may only be removed once " + str(MINIMUM_DELETION_DAYS_SINCE_RESPONSE_VIEW) + " days have passed since their response was first viewed.", 
                   }

LINEUP_STATUS_CHOICES = {
                         0:'Initialization In Progress',
                         1:'Initialized',
                         2:'Sorry, we do not have enough information about your admirer to create a lineup yet.  You can try again in 12 hours.',
                         3:'Sorry, you do not have enough friends to create a lineup at this time.  You can try again in 15 minutes.',
                         4:'Sorry, we are having difficulty getting data from Facebook to create a lineup.  Please try again in a few minutes.',
                         5:'Sorry, we are having difficulty initializing a lineup.  Please try again in a few minutes.', # temporary failure - user can restart lineup initialization
                         }

FEATURES = {
    '1': {
        'NAME': 'View the rest of your lineup', 
        'COST': 1,      
    },
    '2': {
        'NAME':'View your crush\'s response',
        'COST': 1,
    },
    '3': {
        'NAME':"See why your crush isn't interested",
        'COST': 1,
    },
    '4': {
        'NAME':"Converse for 2 Weeks",
        'COST': 2,
    },
    '5': {
        'NAME':"Invite you crush via Facebook",
        'COST': 1,
    },
}

AJAX_ERROR = "Sorry, there is a problem with our servers.  We are working to fix this problem a.s.a.p."
GENERIC_ERROR = "Sorry, we are experiencing difficulty with our servers.  We are working to fix this problem a.s.a.p."

# TODO - THESE MUST BE SET
#RESOURCES_DIR = '/media/shared/src/django-paypal-store-example/samplesite/resources/'
#PAYPAL_PDT_TOKEN = 'HBfJRGv3GKoo9zF1_5t3uA12VlNyvALbtai1rgbZMrYT3wWGcMeuRMpp324'
PAYPAL_PDT_TOKEN = 'S_u0oAhiSDSQpdeppy9KqYANhD2dhH5pm5prcrCcHH0QSIoXLfrMn5-AD0e'
#PAYPAL_EMAIL = 'buyer1_1344811410_per@gmail.com'
#PAYPAL_EMAIL =  'seller_1344811486_biz@gmail.com'
PAYPAL_EMAIL = 'admin@crushmaven.com'

#PAYPAL_RETURN_URL = 'http://142.255.66.205:443/paypal_pdt_purchase'
#PAYPAL_NOTIFY_URL = 'http://142.255.66.205:443/paypal_ipn_listener/'

PAYPAL_RETURN_URL = 'http://www.crushmaven.com/paypal_pdt_purchase'
PAYPAL_NOTIFY_URL = 'http://www.crushmaven.com/paypal_ipn_listener/'

# sandbox
#PAYPAL_URL = 'https://www.sandbox.paypal.com/au/cgi-bin/webscr'
#PAYPAL_PDT_URL = 'https://www.sandbox.paypal.com/au/cgi-bin/webscr'

# live
PAYPAL_URL = 'https://www.paypal.com/au/cgi-bin/webscr'
PAYPAL_PDT_URL = 'https://www.paypal.com/au/cgi-bin/webscr'

# LOAD development settings that override app settings
#try:
#    from dev_settings import *
#except ImportError:
#    print 'local development settings could not be imported'
#    pass

# POSTMAN SETTINGS
STATUS_PENDING = 'p'
STATUS_ACCEPTED = 'a'
STATUS_REJECTED = 'r'
POSTMAN_SEND_NOTIFICATIONS_FREQUENCY=24#send notifications out once every 24 hours
POSTMAN_DISALLOW_ANONYMOUS=True
POSTMAN_DISALLOW_MULTIRECIPIENTS=True
POSTMAN_DISALLOW_COPIES_ON_REPLY=True
POSTMAN_AUTO_MODERATE_AS=True
POSTMAN_SHOW_USER_AS='get_name'
MAILGUN_API_KEY = 'key-36jm6mhebjbgv2bn58zk4xthvjcygwm1'
MAILGUN_PUBLIC_API_KEY = 'pubkey-80f3u-54ke9amr7-fh8fyn7m3g-o3rw5'

# note that NamesLookup is a class that handles the magic behind the dynamic drop down dialog
AJAX_LOOKUP_CHANNELS={'postman_users':('crush.models.user_models','NamesLookup')}
POSTMAN_AUTOCOMPLETER_APP={
    'name':'ajax_select',
    'field':'AutoCompleteField',
    'arg_name':'channel',
    'arg_default':'postman_users'}
AJAX_SELECT_BOOTSTRAP = True
AJAX_SELECT_INLINES = 'inline'
DATABASES={}
if os.environ.get('DATABASE_URL', None):
    import dj_database_url
    DATABASES['default'] = dj_database_url.config()



    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#except:
#    pass
try:
    from settings_local import *
except ImportError, e:
    print 'Unable to load local_settings.py:', e


