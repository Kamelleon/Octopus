# Generated by Django 4.0.4 on 2022-06-11 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_screen', '0004_alter_camera_password_alter_camera_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='camera',
            name='codec',
        ),
        migrations.RemoveField(
            model_name='camera',
            name='substream',
        ),
        migrations.AddField(
            model_name='camera',
            name='suffix',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]