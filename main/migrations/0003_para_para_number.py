# Generated by Django 3.0.3 on 2020-09-13 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200913_0335'),
    ]

    operations = [
        migrations.AddField(
            model_name='para',
            name='para_number',
            field=models.IntegerField(default=0),
        ),
    ]