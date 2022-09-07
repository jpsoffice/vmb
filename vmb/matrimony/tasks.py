from config import celery_app

from django.utils import timezone


@celery_app.task()
def send_batch_matches_emails():
    from .models import Match, Male, Female

    for male_id in (
        Match.objects.filter(status="TSG").values_list("male", flat=True).distinct()
    ):
        male = Male.objects.get(id=male_id)
        male.send_batch_matches_email()

    for female_id in (
        Match.objects.filter(status="TSG").values_list("female", flat=True).distinct()
    ):
        female = Female.objects.get(id=female_id)
        female.send_batch_matches_email()

    Match.objects.filter(status="TSG").update(
        status="SUG", notified=True, notification_time=timezone.now()
    )
