# Generated by Django 3.1.7 on 2021-03-24 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phase1_start', models.DateField()),
                ('phase1_end', models.DateTimeField()),
                ('phase1_group_name', models.CharField(max_length=150)),
                ('phase2_start', models.DateTimeField()),
                ('phase2_end', models.DateTimeField()),
                ('phase2_group_name', models.CharField(max_length=150)),
                ('phase3_start', models.DateTimeField()),
            ],
        ),
    ]