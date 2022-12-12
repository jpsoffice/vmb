from django.db import models

# Create your models here.
from tos.models import UserAgreement

def __str__(self):
    return '%s agreed to TOS: %s' % (self.user.username, str(self.terms_of_service))

UserAgreement.__str__ = __str__