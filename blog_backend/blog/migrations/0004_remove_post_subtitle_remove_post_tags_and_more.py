# Generated by Django 4.2.20 on 2025-05-16 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='subtitle',
        ),
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
