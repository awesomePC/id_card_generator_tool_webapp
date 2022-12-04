# Generated by Django 4.1.3 on 2022-12-04 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('kt_auth', '0002_alter_users_role_delete_userroles'),
        ('dataset', '0004_remove_exporteddataset_created_by_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExportedDataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='name of dataset ex. pan_card_format_1_10k', max_length=255, null=True)),
                ('type', models.CharField(choices=[('detection', 'Detection'), ('recognition', 'Recognition')], help_text='type of dataset 1) detection 2) recognition', max_length=15)),
                ('annotation_type', models.CharField(choices=[('line_level', 'Line Level'), ('word_level', 'Word Level')], help_text='type of annotation either line_level or word_level', max_length=15)),
                ('annotation_format', models.CharField(choices=[('icdar2015', 'ICDAR 2015'), ('ppocrlabel', 'PPOCR Label'), ('easyocr', 'EasyOCR'), ('mmocr', 'MMOCR')], help_text='format of annotation to export such as ppocrlabel, icdar2015, easyocr, mmocr etc..', max_length=15)),
                ('desc', models.TextField(blank=True, help_text='Description of dataset', null=True)),
                ('desc_html', models.TextField(blank=True, help_text='Description of dataset in html format', null=True)),
                ('train_set_percentage', models.PositiveIntegerField(blank=True, default=70, help_text='Training set percentage', null=True)),
                ('val_set_percentage', models.PositiveIntegerField(blank=True, default=15, help_text='Validation set percentage', null=True)),
                ('test_set_percentage', models.PositiveIntegerField(blank=True, default=15, help_text='Testing set percentage', null=True)),
                ('out_directory_path', models.TextField(blank=True, help_text='Root Folder path to store images and other files -- can be auto generated', null=True)),
                ('exported_file_format', models.CharField(blank=True, choices=[('.zip', '.zip'), ('.tar', '.tar'), ('.tar.gz', '.tar.gz')], default='.zip', help_text='format of compressed file such as .zip, .tar etc', max_length=15, null=True)),
                ('exported_file', models.FileField(upload_to='exported_dataset/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by_user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='kt_auth.users')),
                ('source_datasets', models.ManyToManyField(blank=True, help_text='source dataset that has been used to export this data. It amy be one or more', related_name='source_datasets', to='dataset.dataset')),
            ],
        ),
    ]
