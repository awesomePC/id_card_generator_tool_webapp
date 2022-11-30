# Generated by Django 4.1.3 on 2022-11-30 06:15

import annotation.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kt_tasks', '0004_alter_tasks_mainimagefile_and_more'),
        ('annotation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LineAnnotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_index', models.IntegerField(blank=True, help_text='Line index in image', null=True)),
                ('type', models.CharField(choices=[('text', 'text'), ('image', 'image')], help_text='type of bounding box -- what bounding box holding 1) text 2) image', max_length=5)),
                ('text', models.CharField(blank=True, help_text='text if content type is `text`', max_length=255, null=True)),
                ('is_fixed_text', models.BooleanField(default=False)),
                ('is_render_text', models.BooleanField(default=True)),
                ('box_coordinates', models.TextField(blank=True, help_text='Bounding box coordinates. TODO. use ArrayField or JSONfield later', null=True)),
                ('key_label', models.CharField(blank=True, default='OTHER', help_text='Key name for structured data training purpose ex. PERSON_NAME, BIRTH_DATE etc..', max_length=255, null=True)),
                ('cropped_image', models.ImageField(blank=True, null=True, upload_to=annotation.models.cropped_line_image_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dict', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='annotation.dictionaryhub')),
                ('task', models.ForeignKey(blank=True, help_text='Task id in which this line annotation belongs', on_delete=django.db.models.deletion.DO_NOTHING, to='kt_tasks.tasks')),
            ],
        ),
        migrations.RenameModel(
            old_name='WordAnnotations',
            new_name='WordAnnotation',
        ),
        migrations.DeleteModel(
            name='LineAnnotations',
        ),
    ]
