# Generated by Django 4.2.16 on 2024-11-06 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HustRava_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='sub_comments',
        ),
        migrations.RemoveField(
            model_name='post',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
        migrations.AddField(
            model_name='post',
            name='is_topped',
            field=models.BooleanField(default=False, verbose_name='置顶帖子'),
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
