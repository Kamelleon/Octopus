# Generated by Django 4.0.4 on 2022-06-11 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_screen', '0005_remove_camera_codec_remove_camera_substream_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='camera',
            old_name='suffix',
            new_name='ender',
        ),
    ]
