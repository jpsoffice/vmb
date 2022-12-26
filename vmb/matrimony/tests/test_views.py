import pytest
from django.urls import reverse
from vmb.users.forms import UserCreationForm
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from tos.models import *
from vmb.matrimony.models.profiles import *
import datetime
from vmb.matrimony.tests.factories import *
import datetime
from notifications.signals import notify
import json

pytestmark = pytest.mark.django_db


def Reusable_Profile_Generator():

    user = UserCustomFactory()
    profile = MatrimonyFactory(user=user, profile_id=user.username)
    EmailAddress.objects.create(
        user=profile.user, email=profile.user.email, primary=True, verified=True
    )
    tos = TermsOfService.objects.create(active=True, content="This is the new TOS.")
    UserAgreement.objects.create(user=profile.user, terms_of_service=tos)
    return profile


def test_index_view(client):

    # Without Login

    response = client.get(reverse("matrimony:index"), follow=True)

    assert response.status_code == 200
    assert "account/login.html" in (t.name for t in response.templates)

    # With Login
    
    profile = Reusable_Profile_Generator()

    client.login(username=profile.user.username, password="wordpass123")
    response = client.get(reverse("matrimony:index"), follow=True)

    assert response.status_code == 200
    assert "matrimony/profile_edit.html" in (t.name for t in response.templates)


def test_profile_details_view(client):

    profile = Reusable_Profile_Generator()

    # Without Login

    response = client.get(reverse('matrimony:profile-details',args=[profile.profile_id]), follow=True)

    assert response.status_code == 200
    assert "account/login.html" in (t.name for t in response.templates)

    # With Login

    client.login(username=profile.user.username, password="wordpass123")

    response = client.get(reverse('matrimony:profile-details',args=[profile.profile_id]), follow=True)

    assert response.status_code == 200
    assert "matrimony/profile_details.html" in (t.name for t in response.templates)

def test_profile_edit_basic_get_view(client):

    profile = Reusable_Profile_Generator()

    client.login(username=profile.user.username, password="wordpass123")

    response = client.get(reverse('matrimony:profile-edit',args=['basic']), follow=True)

    assert response.status_code == 200
    assert 'matrimony/profile_edit.html' in (t.name  for t in response.templates)

def test_profile_edit_basic_post_view(client, django_db_setup):

    profile = Reusable_Profile_Generator()

    client.login(username=profile.user.username, password="wordpass123")

    response = client.post(
        reverse('matrimony:profile-edit',args=['basic']), 
        data = { 
            'spiritual_name': ['Vaibhav'], 'ethnic_origin': ['57'], 'mother_tongue': ['107'], 'languages_can_speak': ['38', '58', '107'], 'languages_can_read_write': ['38', '58', '107'], 'rounds_chanting': ['25'], 'spiritual_status': ['A'], 'spiritual_master': ['1'], 'children_count': ['0'], 'height': ['167.00'], 'weight': ['70.00'], 'body_type': ['AVG'], 'complexion': ['WHB'], 'current_place_0': ['Nashik, Maharashtra, India'], 'current_place_1': ['19.9974533'], 'current_place_2': ['73.78980229999999'], 'current_city': ['Nashik'], 'current_state': ['Maharashtra'], 'current_country': ['57'], 'nationality': ['57'], 'personality': ['I am Vaibhav Dashrath Mohite'], 'recreational_activities': ['Trekking'], 'devotional_services': ['Cleaning'], 'want_children': ['Y'], 'medical_history': ['Random History'], 'submit': ['Next']
        },
        follow=True
        )

    assert response.redirect_chain[0][0] == reverse('matrimony:profile-edit',args=['profession'])
    assert response.redirect_chain[0][1] == 302
    assert response.status_code == 200

def test_profile_edit_profession_post_view(client, django_db_setup):

    profile = Reusable_Profile_Generator()

    client.login(username=profile.user.username, password="wordpass123")

    response = client.post(
        reverse('matrimony:profile-edit',args=['profession']), 
        data = { 
            'occupations': ['65'], 'employed_in': ['PVT'], 'organization': ['9Island Technologies'], 'annual_income_0': ['30000'], 'annual_income_1': ['INR'], 'occupation_details': ['I am a Django Back-end Developer'], 'education': ['6'], 'institution': ['Indian Institute of Technology, Kharagpur'], 'education_details': ['I am a Mechanical Engineer.'], 'submit': ['Next']
        },
        follow=True
        )
        
    assert response.redirect_chain[0][0] == reverse('matrimony:profile-edit',args=['religion-and-family'])
    assert response.redirect_chain[0][1] == 302
    assert response.status_code == 200

def test_profile_edit_religion_and_family_post_view(client, django_db_setup):

    profile = Reusable_Profile_Generator()

    client.login(username=profile.user.username, password="wordpass123")

    response = client.post(
        reverse('matrimony:profile-edit',args=['religion-and-family']), 
        data = { 
            'religion': ['1'], 'caste': [''], 'caste_other': ['Maratha'], 'subcaste': [''], 'subcaste_other': ['Something'], 'is_tob_unknown': ['True'], 'tob': ['7:20:23'], 'birth_place_0': ['Vaduj, Maharashtra, India'], 'birth_place_1': ['17.593548'], 'birth_place_2': ['74.45109719999999'], 'birth_city': ['Vaduj'], 'birth_state': ['Maharashtra'], 'birth_country': ['57'], 'religious_background': ['Hindu'], 'are_parents_devotees': ['Y'], 'family_values': ['MOD'], 'family_type': ['NF'], 'family_status': ['MC'], 'father_status': ['EMP'], 'mother_status': ['HMK'], 'brothers': ['1'], 'brothers_married': ['0'], 'sisters': ['0'], 'sisters_married': ['0'], 'family_location': ['SAME'], 'family_origin': ['Talbid, Karad'], 'family_details': ['I have a good family.'], 'mentor_1_name': ['Someone'], 'mentor_1_phone': ['2345678901'], 'mentor_1_email': ['email@gmail.com'], 'mentor_2_name': ['Someone 1'], 'mentor_2_phone': ['5647382910'], 'mentor_2_email': ['email@gmail.com'], 'submit': ['Next']
        },
        follow=True
        )
        
    assert response.redirect_chain[0][0] == reverse('matrimony:profile-edit',args=['photos'])
    assert response.redirect_chain[0][1] == 302
    assert response.status_code == 200

def test_profile_edit_expectations_post_view(client, django_db_setup):

    profile = Reusable_Profile_Generator()

    client.login(username=profile.user.username, password="wordpass123")

    response = client.post(
        reverse('matrimony:profile-edit',args=['expectations']), 
        data = { 
            'age_from': ['26'], 'age_to': ['28'], 'height_from': ['160'], 'height_to': ['165'], 'religions': ['7', '1', '5'], 'mother_tongues': ['19', '38', '54', '58', '84', '105', '107', '156', '157'], 'countries_living_in': ['57'], 'ethnicities': ['57'], 'marital_status': ['UMR'], 'want_nri': [''], 'languages_can_speak': ['38', '58', '107'], 'languages_can_read_write': ['38', '58', '107'], 'education': ['0', '18', '50', '1', '75'], 'occupations': ['19', '18', '41', '15', '33', '65'], 'employed_in': ['PSU', 'PVT', 'BUS', 'DEF', 'SE'], 'annual_income_from_0': ['600000'], 'annual_income_from_1': ['INR'], 'annual_income_to_0': ['1500000'], 'annual_income_to_1': ['INR'], 'spiritual_status': ['A'], 'min_rounds_chanting': ['25'], 'spiritual_masters': ['1'], 'partner_description': ['Should be simple and educated.'], 'submit': ['Submit']
        },
        follow=True
        )

    assert response.redirect_chain[0][0] == "/"
    assert response.redirect_chain[0][1] == 302
    assert "Thank you! Your registration has been submitted." in [m.message for m in response.context['messages']]
    assert response.status_code == 200

def test_view_all_notifications_get_view(client, django_db_setup):

    profile = Reusable_Profile_Generator()

    client.login(username=profile.user.username, password="wordpass123")

    response = client.get(reverse("matrimony:view_all_notifications"), follow=True)

    assert response.status_code == 200
    assert "matrimony/view_all_notifications.html" in (t.name for t in response.templates)

def test_mark_all_as_read_view(client, django_db_setup):

    profile = Reusable_Profile_Generator()

    client.login(username=profile.user.username, password="wordpass123")

    notify.send(
        sender=profile.user,
        recipient=profile.user, 
        verb="registration", 
        action_object=profile, 
        target=profile, 
        level="Success", 
        description="Your registration has been successful!", 
        public=True, 
        timestamp=datetime.datetime.now(), 
    )
    
    assert len(profile.user.notifications.unread()) == 1

    response = client.get(reverse("matrimony:mark_all_as_read"), HTTP_REFERER='http://127.0.0.1:8000/view_all_notifications/',follow=True)

    assert len(profile.user.notifications.unread()) == 0
    assert response.status_code == 200
    assert "matrimony/view_all_notifications.html" in (t.name for t in response.templates)

def test_mark_as_read_view(client, django_db_setup):

    profile = Reusable_Profile_Generator()

    client.login(username=profile.user.username, password="wordpass123")

    notify.send(
        sender=profile.user,
        recipient=profile.user, 
        verb="registration", 
        action_object=profile, 
        target=profile, 
        level="Success", 
        description="Your registration has been successful!", 
        public=True, 
        timestamp=datetime.datetime.now(), 
    )
    notify.send(
        sender=profile.user,
        recipient=profile.user, 
        verb="update", 
        action_object=profile, 
        target=profile, 
        level="Success", 
        description="Your update has been successful!", 
        public=True, 
        timestamp=datetime.datetime.now(), 
    )

    assert len(profile.user.notifications.unread()) == 2

    response = client.get(reverse("matrimony:mark_as_read", args=[profile.user.notifications.unread()[0].id]), HTTP_REFERER='http://127.0.0.1:8000/view_all_notifications/',follow=True)

    assert len(profile.user.notifications.unread()) == 1
    assert response.status_code == 200
    assert "matrimony/view_all_notifications.html" in (t.name for t in response.templates)
