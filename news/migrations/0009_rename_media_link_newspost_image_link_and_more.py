# Generated by Django 4.0.3 on 2022-03-05 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_alter_newspost_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newspost',
            old_name='media_link',
            new_name='image_link',
        ),
        migrations.AddField(
            model_name='newspost',
            name='video_link',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]