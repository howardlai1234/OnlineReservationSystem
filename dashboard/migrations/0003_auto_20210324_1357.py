# Generated by Django 3.1.7 on 2021-03-24 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_config'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='phase1_start',
            field=models.DateTimeField(),
        ),
    ]
