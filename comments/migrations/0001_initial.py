# Generated by Django 3.0.3 on 2020-04-04 01:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0002_auto_20200325_1037'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('auth_id', models.TextField(blank=True, max_length=300)),
                ('url', models.TextField(blank=True, max_length=300)),
                ('host', models.TextField(blank=True, max_length=300)),
                ('name', models.TextField(blank=True, max_length=300)),
                ('github', models.TextField(blank=True, max_length=300)),
                ('content', models.TextField(blank=True, max_length=300)),
                ('comment', models.TextField(blank=True, max_length=300)),
                ('published', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('root', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.Posts')),
            ],
        ),
    ]
