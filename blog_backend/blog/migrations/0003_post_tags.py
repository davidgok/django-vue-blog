# Generated by Django 4.2.20 on 2025-05-16 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_subtitle_alter_post_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
