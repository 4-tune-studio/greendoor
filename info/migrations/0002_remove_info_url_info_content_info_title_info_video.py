# Generated by Django 4.0 on 2022-04-04 13:09

import embed_video.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("info", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="info",
            name="url",
        ),
        migrations.AddField(
            model_name="info",
            name="content",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="info",
            name="title",
            field=models.CharField(default="", max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="info",
            name="video",
            field=embed_video.fields.EmbedVideoField(default=""),
            preserve_default=False,
        ),
    ]
