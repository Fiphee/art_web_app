from django.core.management import BaseCommand
from django.contrib.auth import get_user_model

AuthUserModel = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        admin = AuthUserModel.objects.get(username='admin')
        admin.notifications.filter().update(seen=False)
