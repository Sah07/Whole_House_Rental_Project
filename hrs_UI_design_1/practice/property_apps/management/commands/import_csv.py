import csv
from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from property_apps.models import Property

class Command(BaseCommand):
    help = 'Import properties from CSV file'

    def handle(self, *args, **kwargs):
        csv_path = r'C:\Users\my pc\Downloads\house rental app\hrs_UI_design\practice\property_apps\properties.csv'

        try:
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for i, row in enumerate(reader, start=1):
                    try:
                        # Get or fallback to 'admin' user
                        landlord_username = row.get('landlord', '').strip()

                        if landlord_username:
                            user = User.objects.get(username=landlord_username)
                        else:
                            user, created = User.objects.get_or_create(
                                username='admin',
                                defaults={'email': 'admin@example.com'}
                            )
                            if created:
                                user.set_password('admin123')
                                user.save()

                        # Parse date
                        raw_date = row.get('available_from', '2025-01-01')
                        available_from = datetime.strptime(raw_date, "%m/%d/%Y").date()

                        # Parse rent
                        rent_str = row.get('monthly_rent', '0').strip().replace(',', '')
                        monthly_rent = Decimal(rent_str)

                        # Use city if available, or extract from address
                        city = row.get('city', '').strip()
                        if not city:
                            address = row.get('address', 'Unknown').strip()
                            city = address.split(',')[0].strip()
                        else:
                            city = city.split(',')[0].strip()

                        # Create property
                        Property.objects.create(
                            landlord=user,
                            title=row.get('title', 'Untitled Property'),
                            property_type=row.get('property_type', 'Unknown'),
                            address=row.get('address', 'Unknown'),
                            city=city,
                            bedrooms=int(row.get('bedrooms', 0)),
                            bathrooms=int(row.get('bathrooms', 0)),
                            furnished=row.get('furnished', 'false').strip().lower() in ['true', '1', 'yes'],
                            monthly_rent=monthly_rent,
                            available_from=available_from,
                            is_available=row.get('is_available', 'true').strip().lower() in ['true', '1', 'yes'],
                            image=row.get('image', '')
                        )

                        self.stdout.write(f"✅ Row {i} imported successfully.")

                    except Exception as e:
                        self.stderr.write(f"❌ Error on row {i}: {row} → {e}")

            self.stdout.write(self.style.SUCCESS("✅ CSV import completed."))

        except FileNotFoundError:
            self.stderr.write(f"❌ File not found: {csv_path}")
