from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = (
        "Repairs djongo's auto-increment counter for accounts_customuser. "
        "djongo only sets up the '__schema__' auto-increment doc when it "
        "creates a collection for the first time; if the collection already "
        "existed (e.g. from an earlier broken deploy), new rows fall back to "
        "using Mongo's raw ObjectId as the integer primary key, which breaks "
        "auth. This wipes the (currently unusable) accounts_customuser "
        "collection and reinitializes the counter at 0."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--table', default='accounts_customuser',
            help="Collection/table name to repair (default: accounts_customuser)",
        )

    def handle(self, *args, **options):
        table = options['table']

        connection.cursor()  # ensure the underlying pymongo connection is open
        db = connection.connection

        existing = db[table].count_documents({})
        db.drop_collection(table)
        db.create_collection(table)
        self.stdout.write(f"Dropped and recreated '{table}' ({existing} row(s) removed).")

        db['__schema__'].update_one(
            {'name': table},
            {'$set': {'auto': {'field_names': ['id'], 'seq': 0}}},
            upsert=True,
        )
        self.stdout.write(self.style.SUCCESS(
            f"Reinitialized auto-increment counter for '{table}'."
        ))
