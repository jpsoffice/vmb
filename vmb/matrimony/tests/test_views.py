import pytest
from django.urls import reverse
from vmb.users.forms import UserCreationForm
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from tos.models import *
from vmb.matrimony.models.profiles import *
import datetime
from vmb.matrimony.tests.factories import *

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


