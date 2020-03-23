# Generated by Django 3.0.3 on 2020-03-23 19:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('domain', models.URLField(max_length=300, unique=True)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField(blank=True, max_length=300)),
                ('content', models.TextField(blank=True, max_length=300)),
                ('visibility', models.TextField(blank=True, default='PUBLIC', max_length=300)),
                ('visibleTo', models.TextField(blank=True, max_length=300)),
                ('image', models.TextField(blank=True, max_length=300)),
                ('published', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('author_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
