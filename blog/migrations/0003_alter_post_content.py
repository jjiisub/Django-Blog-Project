# Generated by Django 4.2.3 on 2023-07-18 12:06

from django.db import migrations
import django_tuieditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_rename_user_comment_writer_rename_user_post_writer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=django_tuieditor.models.MarkdownField(),
        ),
    ]