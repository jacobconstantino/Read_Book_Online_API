# Generated by Django 3.2.8 on 2021-12-24 07:02

from django.db import migrations, models
import djongo.models.fields
import users_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('name', djongo.models.fields.EmbeddedField(model_container=users_app.models.Name)),
                ('phone_number', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=20)),
                ('agent', models.CharField(max_length=255)),
                ('date_of_birth', models.DateField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=100, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
