# Generated by Django 4.1.3 on 2022-11-30 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kt_tasks', '0004_alter_tasks_mainimagefile_and_more'),
        ('dataset', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DatasetResources',
            new_name='DatasetResource',
        ),
    ]
