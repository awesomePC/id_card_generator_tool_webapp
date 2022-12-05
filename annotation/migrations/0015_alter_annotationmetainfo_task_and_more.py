# Generated by Django 4.1.3 on 2022-12-04 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kt_tasks', '0008_remove_tasks_is_line_annotation_done_and_more'),
        ('kt_auth', '0002_alter_users_role_delete_userroles'),
        ('annotation', '0014_alter_lineannotation_dict_alter_lineannotation_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotationmetainfo',
            name='task',
            field=models.ForeignKey(blank=True, help_text='Task id in which this line annotation belongs', on_delete=django.db.models.deletion.CASCADE, to='kt_tasks.tasks'),
        ),
        migrations.AlterField(
            model_name='dictionaryhub',
            name='created_by_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='createdByUser', to='kt_auth.users'),
        ),
        migrations.AlterField(
            model_name='dictionaryhub',
            name='updated_by_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updatedByUser', to='kt_auth.users'),
        ),
        migrations.AlterField(
            model_name='fonthub',
            name='lang',
            field=models.ForeignKey(blank=True, help_text='Language in which this font file belongs', on_delete=django.db.models.deletion.CASCADE, to='annotation.languagehub'),
        ),
        migrations.AlterField(
            model_name='lineannotationextrainfo',
            name='line',
            field=models.ForeignKey(blank=True, help_text='Line annotation for which we are saving extra information', on_delete=django.db.models.deletion.CASCADE, to='annotation.lineannotation'),
        ),
        migrations.AlterField(
            model_name='linerendering',
            name='line',
            field=models.ForeignKey(blank=True, help_text='Line annotation for which we are rendering this line', on_delete=django.db.models.deletion.CASCADE, to='annotation.lineannotation'),
        ),
        migrations.AlterField(
            model_name='linerenderingpart',
            name='font',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='annotation.fonthub'),
        ),
        migrations.AlterField(
            model_name='linerenderingpart',
            name='lang',
            field=models.ForeignKey(blank=True, help_text='Language of word', on_delete=django.db.models.deletion.CASCADE, to='annotation.languagehub'),
        ),
        migrations.AlterField(
            model_name='linerenderingpart',
            name='line',
            field=models.ForeignKey(blank=True, help_text='Line annotation for which we are rendering this line', on_delete=django.db.models.deletion.CASCADE, to='annotation.lineannotation'),
        ),
        migrations.AlterField(
            model_name='wordannotation',
            name='font',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='annotation.fonthub'),
        ),
        migrations.AlterField(
            model_name='wordannotation',
            name='lang',
            field=models.ForeignKey(blank=True, help_text='Language of word', on_delete=django.db.models.deletion.CASCADE, to='annotation.languagehub'),
        ),
        migrations.AlterField(
            model_name='wordannotation',
            name='task',
            field=models.ForeignKey(blank=True, help_text='Task id in which this line annotation belongs', on_delete=django.db.models.deletion.CASCADE, to='kt_tasks.tasks'),
        ),
    ]
