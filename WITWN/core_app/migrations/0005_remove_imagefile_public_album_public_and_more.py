# Generated by Django 5.2.1 on 2025-06-10 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0004_albumtheme_imagefile_public_album_albumimagefile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagefile',
            name='public',
        ),
        migrations.AddField(
            model_name='album',
            name='public',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='year',
            field=models.IntegerField(null=True),
        ),
    ]
