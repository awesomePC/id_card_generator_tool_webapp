# Generated by Django 4.1.3 on 2022-11-28 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kt_tasks', '0003_alter_tasks_mainimagefile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='MainImageFile',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='TextRemovedImageFile',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
