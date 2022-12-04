# Generated by Django 4.1.3 on 2022-12-04 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0012_remove_annotationmetainfo_grouped_word_annotation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lineannotationextrainfo',
            name='grouped_words_annotation_by_line',
            field=models.ManyToManyField(blank=True, help_text='Word annotation ids that are been grouped together as per line coordinates', related_name='grouped_words_annotation_by_line', to='annotation.wordannotation'),
        ),
    ]
