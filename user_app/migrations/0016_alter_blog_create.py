# Generated by Django 4.0 on 2022-01-05 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0015_alter_blog_index_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='create',
            field=models.DateField(auto_now_add=True),
        ),
    ]
