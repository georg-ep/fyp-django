# Generated by Django 3.2.6 on 2023-03-13 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0015_auto_20230313_1158'),
    ]

    operations = [
        migrations.RenameField(
            model_name='breathingexercise',
            old_name='descritption',
            new_name='description',
        ),
    ]
