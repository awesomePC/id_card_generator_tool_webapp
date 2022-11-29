# Generated by Django 4.1.3 on 2022-11-29 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('kt_auth', '0002_alter_users_role_delete_userroles'),
        ('dataset', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingHub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='name of training', max_length=255, null=True)),
                ('desc', models.TextField(blank=True, help_text='Description of Training', null=True)),
                ('remote_ip', models.CharField(blank=True, help_text='Remote GPU server ip to connect for distributed training', max_length=255, null=True)),
                ('gpu_ids', models.CharField(blank=True, help_text='Comma separated list of GPU id', max_length=255, null=True)),
                ('input_checkpoint_file', models.FileField(blank=True, help_text='model checkpoint for resuming training if any', null=True, upload_to='checkpoints/input/')),
                ('output_checkpoint_file', models.FileField(blank=True, help_text='output directory to store model checkpoint', null=True, upload_to='checkpoints/output/')),
                ('status', models.CharField(blank=True, choices=[('not-started', 'not-started'), ('ready', 'ready'), ('started', 'started'), ('running', 'running'), ('successful', 'successful'), ('failed', 'failed'), ('aborted', 'aborted')], help_text='Status of process', max_length=15, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by_user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='kt_auth.users')),
                ('dataset', models.ForeignKey(blank=True, help_text='dataset on which we are performing training', on_delete=django.db.models.deletion.DO_NOTHING, to='dataset.exporteddataset')),
            ],
        ),
    ]
