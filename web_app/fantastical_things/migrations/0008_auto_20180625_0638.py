# Generated by Django 2.0.6 on 2018-06-25 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fantastical_things', '0007_auto_20180625_0225'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='month',
            new_name='months',
        ),
    ]
