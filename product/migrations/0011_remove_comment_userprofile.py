# Generated by Django 3.0.3 on 2020-05-18 23:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_auto_20200518_2354'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='userprofile',
        ),
    ]
