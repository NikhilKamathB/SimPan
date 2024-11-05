# Generated by Django 5.1 on 2024-11-05 05:54

import django.db.models.deletion
import uuid
import workspace.utils
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Studio',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('conversation', models.JSONField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='studio_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Studio',
                'verbose_name_plural': 'Studios',
            },
        ),
        migrations.CreateModel(
            name='StudioStorage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to=workspace.utils.get_studio_file_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('studio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studio_files', to='workspace.studio')),
            ],
            options={
                'verbose_name': 'Studio Storage',
                'verbose_name_plural': 'Studio Storages',
            },
        ),
    ]
