from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create superuser mzs/mzs'

    def handle(self, *args, **kwargs):
        if User.objects.filter(username='mzs').exists():
            u = User.objects.get(username='mzs')
            u.set_password('mzs')
            u.is_superuser = True
            u.is_staff = True
            u.save()
            self.stdout.write(self.style.SUCCESS('Password reset to mzs'))
        else:
            User.objects.create_superuser('mzs', '', 'mzs')
            self.stdout.write(self.style.SUCCESS('Superuser mzs created'))
