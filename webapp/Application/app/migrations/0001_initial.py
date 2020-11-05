# Generated by Django 3.0.5 on 2020-10-22 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User_profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('confirm_password', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=30)),
                ('zipcode', models.CharField(max_length=10)),
                ('dob', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('height', models.DecimalField(decimal_places=3, max_digits=10)),
                ('weight', models.DecimalField(decimal_places=3, max_digits=10)),
            ],
        ),
    ]