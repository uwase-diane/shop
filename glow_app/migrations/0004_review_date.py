# Generated by Django 3.1.7 on 2021-03-26 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glow_app', '0003_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
