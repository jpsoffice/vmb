from config import celery_app

from .models import Match, Male, Female


@celery_app.task()
def send_batch_match_emails():
    for male_id in Match.objects.filter(status='TON').values_list('male', flat=True).distinct():
        male = Male.objects.get(id=male_id)
        male.send_batch_matches_email()
        male.female_matches.filter(status='TON').update(status='NOT')

    for female_id in Match.objects.filter(status='TON').values_list('female', flat=True).distinct():
        female = Female.objects.get(id=female_id)
        female.send_batch_matches_email()
        female.male_matches.filter(status='TON').update(status='NOT')
