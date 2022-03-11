# Generated by Django 4.0 on 2022-03-11 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='feedbookmark',
            constraint=models.UniqueConstraint(fields=('user_id', 'feed_id'), name='unique_user_feedbookmark'),
        ),
        migrations.AddConstraint(
            model_name='feedlike',
            constraint=models.UniqueConstraint(fields=('user_id', 'feed_id'), name='unique_user_feedlike'),
        ),
    ]
