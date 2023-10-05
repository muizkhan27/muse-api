# Generated by Django 4.1.7 on 2023-03-02 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, null=True)),
                ('email', models.EmailField(max_length=100, null=True, unique=True)),
                ('password', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('subdomain', models.CharField(default='', max_length=100, unique=True)),
            ],
            options={
                'db_table': 'tenants',
            },
        ),
    ]