# Generated by Django 4.0.4 on 2022-06-03 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_screen', '0002_alter_camera_codec'),
    ]

    operations = [
        migrations.AddField(
            model_name='camera',
            name='port',
            field=models.IntegerField(default=554),
            preserve_default=False,
        ),
    ]
