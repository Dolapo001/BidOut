# Generated by Django 4.2.3 on 2023-09-19 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_alter_category_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.UUIDField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
