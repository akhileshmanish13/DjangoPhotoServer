# Generated by Django 3.1.1 on 2020-09-19 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CachedPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cached_image', models.BinaryField(blank=True, null=True)),
                ('cache_file_url', models.CharField(max_length=500, null=True)),
                ('number_of_times_read', models.IntegerField(default=0)),
                ('date_added', models.DateTimeField(verbose_name='Date published')),
                ('to_delete', models.BooleanField()),
            ],
        ),
    ]
