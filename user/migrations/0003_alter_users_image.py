# Generated by Django 4.0 on 2022-04-02 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_alter_users_groups_alter_users_user_permissions_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="image",
            field=models.CharField(default="img/profile.jpg", max_length=256),
        ),
    ]