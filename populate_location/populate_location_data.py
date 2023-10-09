from django.core.management.base import BaseCommand
import csv
from customers.models import City, State

class Command(BaseCommand):
    help = 'Populate City and State models from your CSV data'

    def handle(self, *args, **options):
        # Modify this path to point to your CSV file
        csv_file_path = 'populate_location/zip_code_database.csv'

        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                state_name = row['state']
                city_name = row['city']

                # Check if the state already exists or create a new one
                state, created = State.objects.get_or_create(name=state_name)

                # Check if the city already exists or create a new one
                city, created = City.objects.get_or_create(name=city_name, state=state)
