# Generated by Django 4.2.4 on 2023-09-03 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ezapp', '0003_customuser_logintoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='loginToken',
            field=models.CharField(max_length=500),
        ),
    ]