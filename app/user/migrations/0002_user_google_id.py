# Generated by Django 3.2.3 on 2021-06-16 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='google_id',
            field=models.CharField(blank=True, default=None, editable=False, max_length=255, null=True, verbose_name='Google ID'),
        ),
    ]
