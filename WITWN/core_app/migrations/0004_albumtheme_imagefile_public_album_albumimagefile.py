# Generated by Django 5.2.1 on 2025-06-10 13:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0003_remove_tag_color_alter_userpost_links'),
        ('user_app', '0010_account_birthday'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlbumTheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='imagefile',
            name='public',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.account')),
                ('theme', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core_app.albumtheme')),
            ],
        ),
        migrations.CreateModel(
            name='AlbumImageFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='albums/')),
                ('public', models.BooleanField(default=True)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_app.album')),
            ],
        ),
    ]
