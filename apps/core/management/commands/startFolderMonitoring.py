from django.core.management.base import BaseCommand
from apps.core.utils import folderMonitoring  # Import your function here
from apps.core.utils import readConfig

class Command(BaseCommand):
    help = 'Run folderMonitoring task'
    def handle(self, *args, **options):
        conf = readConfig()
        folderMonitoring(conf['Settings']['monitoringPath'])
        self.stdout.write(self.style.SUCCESS('Successfully executed folderMonitoring'))
