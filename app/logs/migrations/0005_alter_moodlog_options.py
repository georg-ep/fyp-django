# Generated by Django 3.2.6 on 2023-01-23 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0004_alter_moodlog_datetime'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='moodlog',
            options={'ordering': ['datetime']},
        ),
    ]