# Generated by Django 3.0.3 on 2020-09-12 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='img',
            name='overall_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='para',
            name='overall_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subsection',
            name='Subsection_item_count',
            field=models.IntegerField(default=0),
        ),
    ]
