# Generated by Django 4.0 on 2022-03-11 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0006_alter_plant_extragrow_info_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='insect_info',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]