# Generated by Django 2.1.7 on 2019-04-27 17:34

from django.conf import settings
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('moviealert', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venues', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None)),
                ('movie_name', models.CharField(max_length=200)),
                ('movie_language', models.CharField(choices=[('Hindi', 'Hindi'), ('English', 'English'), ('Tamil', 'Tamil'), ('Punjabi', 'Punjabi'), ('Telugu', 'Telugu'), ('Kannada', 'Kannada'), ('Malayalam', 'Malayalam')], default='Hindi', max_length=20)),
                ('movie_dimension', models.CharField(choices=[('2D', '2D'), ('2D 4DX', '2D 4DX'), ('3D', '3D'), ('3D 4DX', '3D 4DX'), ('IMAX 2D', 'IMAX 2D'), ('IMAX 3D', 'IMAX 3D')], default='2D', max_length=20)),
                ('movie_date', models.DateField()),
                ('task_completed', models.BooleanField(default=False)),
                ('dropped', models.BooleanField(default=False)),
                ('found_time', django.contrib.postgres.fields.jsonb.JSONField(default=list)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubRegion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subregion_code', models.CharField(blank=True, max_length=20, null=True)),
                ('subregion_name', models.CharField(blank=True, max_length=255, null=True)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moviealert.Region')),
            ],
        ),
        migrations.CreateModel(
            name='Theater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('venue_code', models.CharField(blank=True, max_length=20, null=True)),
                ('subregion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moviealert.SubRegion')),
            ],
        ),
        migrations.AlterField(
            model_name='task',
            name='movie_dimension',
            field=models.CharField(choices=[('2D', '2D'), ('2D 4DX', '2D 4DX'), ('3D', '3D'), ('3D 4DX', '3D 4DX'), ('IMAX 2D', 'IMAX 2D'), ('IMAX 3D', 'IMAX 3D')], default='2D', max_length=20),
        ),
    ]
