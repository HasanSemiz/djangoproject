# Generated by Django 3.0.3 on 2020-05-18 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_comment_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='email',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='product',
            name='isim',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='product',
            name='telefon',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]