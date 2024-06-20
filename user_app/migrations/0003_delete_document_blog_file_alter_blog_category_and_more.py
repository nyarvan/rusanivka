# Generated by Django 4.0 on 2024-06-20 03:49

from django.db import migrations, models
import django.db.models.deletion
import user_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0002_alter_blog_options_categoryblog_blog_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.AddField(
            model_name='blog',
            name='file',
            field=models.FileField(null=True, upload_to='files/blogs'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='category',
            field=models.ForeignKey(default=user_app.models.Blog.get_default_category, on_delete=django.db.models.deletion.CASCADE, to='user_app.categoryblog'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(default='images/doctors/no-image.png', null=True, upload_to='images/blogs'),
        ),
    ]
