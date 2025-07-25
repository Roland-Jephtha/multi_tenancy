# Generated by Django 4.2.7 on 2025-07-10 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '0005_apartment_is_occupied'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dependent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('relationship', models.CharField(choices=[('spouse', 'Spouse'), ('child', 'Child'), ('parent', 'Parent'), ('sibling', 'Sibling'), ('other', 'Other')], max_length=20)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('passport_photo', models.ImageField(blank=True, null=True, upload_to='dependent_photos/')),
                ('id_type', models.CharField(choices=[('national_id', 'National ID'), ('voters_card', "Voter's Card"), ('drivers_license', "Driver's License"), ('international_passport', 'International Passport'), ('other', 'Other')], max_length=30)),
                ('id_number', models.CharField(max_length=50)),
                ('medical_notes', models.TextField(blank=True, help_text='Allergies, disabilities, etc.', null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('landlord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dependents', to='landlord.landlord')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
