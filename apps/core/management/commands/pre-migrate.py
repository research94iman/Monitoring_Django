# pre_migrate.py

from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Execute SQL commands before running migrations'

    def handle(self, *args, **options):
        # Execute your SQL commands here
        with connection.cursor() as cursor:
            cursor.execute("DO "
                           "$$ "
                           "BEGIN "
                                "IF NOT EXISTS ( "
                                    "SELECT 1 "
                                    "FROM pg_catalog.pg_database "
                                    "WHERE datname = 'monitoring' "
                                ") THEN "
                                    "CREATE DATABASE monitoring "
                                        "WITH OWNER = postgres  "
                                        "ENCODING = 'UTF8' "
                                        "LOCALE_PROVIDER = 'libc' "
                                        "CONNECTION LIMIT = -1 "
                                        "IS_TEMPLATE = False;"
                                "END IF; "
                           "END;"
                           "$$; "
                           )

        self.stdout.write(self.style.SUCCESS('SQL commands executed successfully'))
