# Generated by Django 4.2.4 on 2023-09-03 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ezapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='uutoken',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
