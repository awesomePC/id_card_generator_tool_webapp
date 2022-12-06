# Generated by Django 4.1.3 on 2022-12-05 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0009_alter_dataset_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasetresource',
            name='dataset',
            field=models.ForeignKey(blank=True, help_text='Dataset in which this image belongs', on_delete=django.db.models.deletion.CASCADE, to='dataset.dataset'),
        ),
    ]
