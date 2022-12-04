# Generated by Django 4.1.3 on 2022-12-04 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0011_annotationmetainfo_grouped_word_annotation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='annotationmetainfo',
            name='grouped_word_annotation',
        ),
        migrations.CreateModel(
            name='LineAnnotationExtraInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('grouped_words_annotation_by_line', models.ManyToManyField(blank=True, help_text='source dataset that has been used to export this data. It amy be one or more', related_name='grouped_words_annotation_by_line', to='annotation.wordannotation')),
                ('line', models.ForeignKey(blank=True, help_text='Line annotation for which we are saving extra information', on_delete=django.db.models.deletion.DO_NOTHING, to='annotation.lineannotation')),
            ],
        ),
    ]