# Generated by Django 2.2.16 on 2022-05-28 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20220525_1403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='slug',
        ),
    ]