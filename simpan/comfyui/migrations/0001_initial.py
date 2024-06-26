# Generated by Django 5.0.4 on 2024-05-04 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CeleryTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=255, unique=True)),
                ('queue_name', models.CharField(max_length=255)),
                ('task_name', models.CharField(max_length=255)),
                ('task_type', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('Initiated', 'Initiated'), ('Completed', 'Completed'), ('Aborted', 'Aborted')], default='Initiated', max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Celery Task',
                'verbose_name_plural': 'Celery Tasks',
            },
        ),
    ]
