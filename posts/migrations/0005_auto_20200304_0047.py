# Generated by Django 2.1.5 on 2020-03-04 00:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20200226_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='publish',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
