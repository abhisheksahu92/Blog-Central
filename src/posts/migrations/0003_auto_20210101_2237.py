# Generated by Django 3.1.4 on 2021-01-01 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_viewcount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='viewcount',
            new_name='views_count',
        ),
    ]
