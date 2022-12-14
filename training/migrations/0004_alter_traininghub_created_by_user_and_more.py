# Generated by Django 4.1.3 on 2022-12-04 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kt_auth', '0002_alter_users_role_delete_userroles'),
        ('export', '0002_alter_exporteddataset_created_by_user'),
        ('training', '0003_alter_traininghub_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traininghub',
            name='created_by_user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='kt_auth.users'),
        ),
        migrations.AlterField(
            model_name='traininghub',
            name='dataset',
            field=models.ForeignKey(blank=True, help_text='dataset on which we are performing training', on_delete=django.db.models.deletion.CASCADE, to='export.exporteddataset'),
        ),
    ]
