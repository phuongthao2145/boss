#https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html
from django.core.management.base import BaseCommand
from django.utils import timezone
from polls.views import sendmail
class Command(BaseCommand):
    help = 'Displays current time'
    def handle(self, *args, **kwargs):
        sendmail()
        time = timezone.now().strftime('%X')
        self.stdout.write("send mail cron 2")