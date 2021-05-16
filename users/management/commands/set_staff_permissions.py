from django.core.management import BaseCommand
from django.contrib.auth.models import Permission, Group
from utils.get_permission_names import get_permission_names
from users.models import Profile, AuthUserModel
from artworks.models import Artwork
from galleries.models import Gallery


class Command(BaseCommand):
    _staff_group_name = 'Staff'


    @staticmethod
    def get_staff_group():
        try:
            staff_group = Group.objects.get(name=Command._staff_group_name)
        except Group.DoesNotExist:
            permission_names = get_permission_names((Profile, Artwork, Gallery))
            permissions = Permission.objects.filter(codename__in=permission_names)

            staff_group = Group(name=Command._staff_group_name)
            staff_group.save()
            staff_group.permissions.set(permissions)
        return staff_group


    def handle(self, *args, **options):
        staff_group = Command.get_staff_group()
        staff_members = AuthUserModel.objects.filter(is_staff=True)
        for staff_member in staff_members:
            if not staff_member.groups.filter(name=Command._staff_group_name).exists():
                staff_member.groups.add(staff_group)
    
