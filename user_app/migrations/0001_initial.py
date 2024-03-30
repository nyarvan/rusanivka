# Generated by Django 4.0 on 2024-01-06 04:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50)),
                ('position', models.PositiveIntegerField()),
                ('image', models.ImageField(default='images/doctors/no-image.png', upload_to='images/administration')),
                ('post', models.CharField(max_length=50)),
                ('schedule', models.TextField(blank=True)),
                ('phone', models.CharField(max_length=25)),
            ],
            options={
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=100)),
                ('image', models.ImageField(default='images/doctors/no-image.png', upload_to='images/blogs')),
                ('text', models.TextField(blank=True)),
                ('create', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-create',),
                'index_together': {('id', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_processing', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-date', 'is_processing'),
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, unique=True)),
                ('full_name', models.CharField(max_length=75, unique=True)),
                ('number', models.PositiveIntegerField(unique=True)),
                ('manager', models.CharField(max_length=50)),
                ('image', models.ImageField(default='images/doctors/no-image.png', upload_to='images/departments')),
                ('phone', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('number',),
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='files/')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50)),
                ('image', models.ImageField(default='images/doctors/no-image.png', upload_to='images/doctors')),
                ('post', models.CharField(max_length=100)),
                ('room', models.CharField(max_length=50)),
                ('schedule', models.TextField(blank=True)),
                ('is_manager', models.BooleanField(default=False)),
                ('is_visible', models.BooleanField(default=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.department')),
            ],
            options={
                'ordering': ('department', '-is_manager', 'is_visible'),
            },
        ),
        migrations.CreateModel(
            name='BlogImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='images/doctors/no-image.png', upload_to='images/blogs')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.blog')),
            ],
            options={
                'ordering': ('-blog',),
            },
        ),
    ]
