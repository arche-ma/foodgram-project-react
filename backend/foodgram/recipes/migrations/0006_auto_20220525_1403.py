# Generated by Django 2.2.16 on 2022-05-25 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20220521_1048'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='in_shopping_card',
            new_name='in_shopping_cart',
        ),
    ]