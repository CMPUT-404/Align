# Generated by Django 3.0.3 on 2020-03-25 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='origin',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='posts',
            name='source',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='image',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='visibility',
            field=models.TextField(blank=True, default='PUBLIC', max_length=300),
        ),
    ]