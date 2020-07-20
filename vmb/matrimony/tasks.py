from config import celery_app

from django.core.mail import send_mail
from django.utils import timezone


@celery_app.task()
def send_batch_matches_emails():
    from .models import Match, Male, Female

    for male_id in (
        Match.objects.filter(status="TON").values_list("male", flat=True).distinct()
    ):
        male = Male.objects.get(id=male_id)
        male.send_batch_matches_email()

    for female_id in (
        Match.objects.filter(status="TON").values_list("female", flat=True).distinct()
    ):
        female = Female.objects.get(id=female_id)
        female.send_batch_matches_email()

    Match.objects.filter(status="TON").update(status="NTF")


@celery_app.task()
def send_email(email_message_id):
    from .models import EmailMessage

    email_message = EmailMessage.objects.get(id=email_message_id)
    send_mail(
        email_message.subject,
        "",
        email_message.sender,
        [email_message.to],
        html_message=email_message.body,
    )
    email_message.status = "SNT"
    email_message.sent_at = timezone.now()
    email_message.save()


@celery_app.task()
def update_rates():
    from .models import CurrencyExchangeRate

    existing_currency = ",".join(
        currency
        for currency in CurrencyExchangeRate.objects.values_list(
            "from_currency", flat=True
        )
    )
    backend = OpenExchangeRatesBackend(url=OPEN_EXCHANGE_RATES_URL)
    backend.update_rates(symbols=existing_currency)

    for obj in CurrencyExchangeRate:
        obj.exchange_rate = get_rate(
            obj.from_currency, "INR", backend=OpenExchangeRatesBackend.name
        )
