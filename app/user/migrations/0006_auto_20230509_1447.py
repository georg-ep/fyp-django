# Generated by Django 3.2.6 on 2023-05-09 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20230507_1340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
        migrations.AddField(
            model_name='user',
            name='email_encrypted',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]
