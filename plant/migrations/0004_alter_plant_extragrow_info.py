# Generated by Django 4.0 on 2022-03-11 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0003_alter_plant_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='extragrow_info',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]
