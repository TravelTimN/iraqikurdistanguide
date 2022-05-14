from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError
from django.conf import settings


class RestrictEmailAdapter(DefaultAccountAdapter):

    def clean_email(self, email):
        admin_emails = settings.ADMIN_EMAILS
        RestrictedList = [x.strip() for x in admin_emails.split(", ")]
        if email not in RestrictedList:
            raise ValidationError(
                "Registration Restricted. Please Contact Admin.")
        return email
