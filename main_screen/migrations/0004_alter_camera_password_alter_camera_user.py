# Generated by Django 4.0.4 on 2022-06-04 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_screen', '0003_camera_port'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='password',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='camera',
            name='user',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]