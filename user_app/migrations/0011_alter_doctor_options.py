# Generated by Django 4.0 on 2022-01-05 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0010_alter_doctor_options_remove_doctor_is_director_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='doctor',
            options={'ordering': ('department', '-is_manager', 'is_visible')},
        ),
    ]
