#https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html
from django.core.management.base import BaseCommand
from django.utils import timezone
from polls.views import createpdf
class Command(BaseCommand):
    help = 'Displays current time'
    def handle(self, *args, **kwargs):
        createpdf()
        time = timezone.now().strftime('%X')
        self.stdout.write("write pdf cron")