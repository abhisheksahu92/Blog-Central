# Generated by Django 3.1.4 on 2020-12-28 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20201228_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='read_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
