# Generated by Django 4.0.4 on 2022-06-02 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_screen', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='codec',
            field=models.CharField(choices=[('h264', 'h264'), ('h265', 'h265')], max_length=4),
        ),
    ]
