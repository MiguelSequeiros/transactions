import csv
from django.core.management import BaseCommand
from django.utils import timezone

from txs.models import Transaction, Company


class Command(BaseCommand):
    help = 'Loads transactions from CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        start_time = timezone.now()
        file_path = options['file_path']
        with open(file_path, 'r') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            next(data) # skip header
            txs = []
            for row in data:
                company_name = row[0]
                company, created = Company.objects.get_or_create(name=company_name)
                available_choices = ['pending', 'closed', 'reversed']
                if row[3] in available_choices:
                    transaction = Transaction(
                        company_id=company.id,
                        price=row[1],
                        date=row[2],
                        state=row[3],
                        approved=True if row[4] == 'true' else False,
                    )
                    txs.append(transaction)
                else:
                    self.stdout.write(
                        self.style.WARNING(f'WRONG STATE: {row}')
                    )


            if txs:
                Transaction.objects.bulk_create(txs)
        end_time = timezone.now()
        self.stdout.write(
            self.style.SUCCESS(
                f'Loading CSV took: {(end_time-start_time).total_seconds()} seconds.'
            )
        )