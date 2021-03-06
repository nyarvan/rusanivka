# Generated by Django 4.0 on 2022-01-05 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0009_alter_blog_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='doctor',
            options={'ordering': ('department', 'is_manager', 'is_visible')},
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='is_director',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='is_extdirector',
        ),
        migrations.AddField(
            model_name='doctor',
            name='is_visible',
            field=models.BooleanField(default=True),
        ),
    ]
