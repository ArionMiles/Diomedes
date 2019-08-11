# Generated by Django 2.1.7 on 2019-08-11 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moviealert', '0007_auto_20190809_0051'),
    ]

    operations = [
        migrations.CreateModel(
            name='TheaterLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('found', models.BooleanField(default=False)),
                ('found_at', models.DateTimeField()),
            ],
        ),
        migrations.RenameField(
            model_name='subregion',
            old_name='subregion_code',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='subregion',
            old_name='subregion_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='theater',
            old_name='venue_code',
            new_name='code',
        ),
        migrations.RemoveField(
            model_name='reminder',
            name='venues',
        ),
        migrations.AddField(
            model_name='theater',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='moviealert.Region'),
        ),
        migrations.AlterField(
            model_name='theater',
            name='subregion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='moviealert.SubRegion'),
        ),
        migrations.AddField(
            model_name='theaterlink',
            name='reminder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moviealert.Reminder'),
        ),
        migrations.AddField(
            model_name='theaterlink',
            name='theater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moviealert.Theater'),
        ),
        migrations.AddField(
            model_name='reminder',
            name='theaters',
            field=models.ManyToManyField(related_name='reminders', through='moviealert.TheaterLink', to='moviealert.Theater'),
        ),
    ]