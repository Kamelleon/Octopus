# Generated by Django 4.0.4 on 2022-06-11 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_screen', '0006_rename_suffix_camera_ender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='camera',
            old_name='ender',
            new_name='suffix',
        ),
    ]
