from infrastructure_views import home
from infrastructure_views import logout_view

# admirer view and process views
from admirer_views import admirers
from admirer_views import ajax_display_lineup_block
from admirer_views import ajax_show_lineup_slider
from admirer_views import ajax_get_lineup_slide
from admirer_views import ajax_add_lineup_member
from admirer_views import ajax_update_num_platonic_friends
from admirer_views import ajax_update_num_crushes_in_progress
from admirer_views import admirers_past

# crush view and creation views
from crush_views import attractions
from crush_views import attractions_completed
from crush_views import app_invite_form
from crush_views import app_invite_form_v2
from crush_views import ajax_find_fb_user

from setup_views import setup_create_form

from platonic_friend_views import ajax_reconsider
from platonic_friend_views import just_friends

from friends_with_admirers_views import friends_with_admirers
from friends_with_admirers_views import ajax_friends_with_admirers_content

from payment_views import ajax_update_num_credits
from payment_views import ajax_deduct_credit
from payment_views import credit_checker
from payment_views import paypal_pdt_purchase
from payment_views import paypal_ipn_listener

from settings_views import settings_profile
from settings_views import settings_notifications
from settings_views import settings_credits

from static_file_views import help_how_it_works
from static_file_views import help_faq
from static_file_views import help_terms
from static_file_views import help_privacy
from static_file_views import help_contact

