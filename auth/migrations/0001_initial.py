# Generated by Django 4.1.3 on 2022-11-26 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserRoles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.TextField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FirstName', models.TextField(blank=True, max_length=255, null=True)),
                ('LastName', models.TextField(blank=True, max_length=255, null=True)),
                ('Email', models.TextField(blank=True, null=True)),
                ('IsActive', models.BooleanField(default=True)),
                ('Password', models.TextField(blank=True, null=True)),
                ('CreatedDate', models.DateTimeField(auto_now=True)),
                ('UpdatedDate', models.DateTimeField(auto_now=True)),
                ('Role', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Users', to='kt_auth.userroles')),
            ],
        ),
    ]