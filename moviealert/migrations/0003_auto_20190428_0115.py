# Generated by Django 2.1.7 on 2019-04-27 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moviealert', '0002_auto_20190427_2304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reminder',
            old_name='task_completed',
            new_name='completed',
        ),
        migrations.RenameField(
            model_name='reminder',
            old_name='movie_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='reminder',
            old_name='movie_dimension',
            new_name='dimension',
        ),
        migrations.RenameField(
            model_name='reminder',
            old_name='movie_language',
            new_name='language',
        ),
        migrations.RenameField(
            model_name='reminder',
            old_name='movie_name',
            new_name='name',
        ),
    ]