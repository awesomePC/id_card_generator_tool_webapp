# Generated by Django 4.1.3 on 2022-12-05 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kt_tasks', '0009_alter_tasks_createbyuserid_alter_tasks_projectid_and_more'),
        ('dataset', '0008_alter_dataset_task_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='task',
            field=models.ForeignKey(blank=True, help_text='Task id in which this dataset belongs', null=True, on_delete=django.db.models.deletion.CASCADE, to='kt_tasks.tasks'),
        ),
    ]
