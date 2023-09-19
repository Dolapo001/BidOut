

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser with the provided username and password'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Superuser username')
        parser.add_argument('password', type=str, help='Superuser password')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        password = kwargs['password']

        try:
            User.objects.create_superuser(username, '', password)
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: {username}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error creating superuser: {str(e)}'))
