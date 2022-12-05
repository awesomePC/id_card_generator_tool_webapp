# Generated by Django 4.1.3 on 2022-12-04 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kt_tasks', '0008_remove_tasks_is_line_annotation_done_and_more'),
        ('annotation', '0013_alter_lineannotationextrainfo_grouped_words_annotation_by_line'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lineannotation',
            name='dict',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='annotation.dictionaryhub'),
        ),
        migrations.AlterField(
            model_name='lineannotation',
            name='task',
            field=models.ForeignKey(blank=True, help_text='Task id in which this line annotation belongs', on_delete=django.db.models.deletion.CASCADE, to='kt_tasks.tasks'),
        ),
    ]
