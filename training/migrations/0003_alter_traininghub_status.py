# Generated by Django 4.1.3 on 2022-12-04 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0002_alter_traininghub_dataset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traininghub',
            name='status',
            field=models.CharField(blank=True, choices=[('not-started', 'not-started'), ('ready', 'ready'), ('started', 'started'), ('running', 'running'), ('completed', 'completed'), ('failed', 'failed'), ('aborted', 'aborted')], help_text='Status of process', max_length=15, null=True),
        ),
    ]
