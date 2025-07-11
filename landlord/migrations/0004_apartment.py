# Generated by Django 4.2.7 on 2025-07-10 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '0003_landlord_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('property_status', models.CharField(choices=[('resident', 'Resident'), ('commercial', 'Commercial'), ('developing', 'Developing'), ('undeveloped', 'Undeveloped')], max_length=20)),
                ('total_floors', models.PositiveIntegerField()),
                ('property_type', models.CharField(choices=[('apartment', 'Apartment'), ('condo', 'Condo'), ('studio', 'Studio'), ('loft', 'Loft'), ('duplex', 'Duplex')], max_length=20)),
                ('total_units', models.PositiveIntegerField()),
                ('special_notes', models.TextField(blank=True, null=True)),
                ('monthly_rent', models.DecimalField(decimal_places=2, max_digits=12)),
                ('security_deposit', models.DecimalField(decimal_places=2, max_digits=12)),
                ('building_picture', models.ImageField(blank=True, null=True, upload_to='apartment_images/')),
                ('lease_term', models.CharField(choices=[('1-year', '1-year'), ('month-to-month', 'Month-to-Month'), ('6-month', '6-month'), ('other', 'Other')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('landlord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apartments', to='landlord.landlord')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
