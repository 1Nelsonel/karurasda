# Generated by Django 4.2.3 on 2023-08-20 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_song_rename_sons_live'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Live',
            new_name='LiveStream',
        ),
    ]
