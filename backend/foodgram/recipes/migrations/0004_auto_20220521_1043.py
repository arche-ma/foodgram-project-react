# Generated by Django 2.2.16 on 2022-05-21 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20220517_1813'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shoppingcart',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='shoppingcart',
            name='recipe',
        ),
        migrations.RemoveField(
            model_name='shoppingcart',
            name='user',
        ),
        migrations.DeleteModel(
            name='Favorite',
        ),
        migrations.DeleteModel(
            name='ShoppingCart',
        ),
    ]