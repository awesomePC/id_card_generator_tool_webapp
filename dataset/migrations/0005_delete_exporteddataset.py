# Generated by Django 4.1.3 on 2022-12-04 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0002_alter_traininghub_dataset'),
        ('dataset', '0004_remove_exporteddataset_created_by_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ExportedDataset',
        ),
    ]
