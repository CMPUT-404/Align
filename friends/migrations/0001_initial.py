# Generated by Django 3.0.3 on 2020-04-05 04:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sender', models.URLField()),
                ('receiver', models.URLField()),
                ('status', models.BooleanField(default=None, null=True)),
            ],
            options={
                'unique_together': {('sender', 'receiver')},
            },
        ),
    ]
