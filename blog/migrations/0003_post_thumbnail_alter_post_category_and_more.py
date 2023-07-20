# Generated by Django 4.2.3 on 2023-07-20 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_rename_user_comment_writer_rename_user_post_writer'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnails/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('HTML/CSS', 'HTML/CSS'), ('Python', 'Python'), ('Django', 'Django'), ('고양이', '고양이')], max_length=50),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]