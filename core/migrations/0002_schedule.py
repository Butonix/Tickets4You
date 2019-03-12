# Generated by Django 2.1.2 on 2019-03-11 16:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
                ('transport_type', models.CharField(max_length=20)),
                ('date', models.CharField(max_length=20)),
                ('json_data', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Schedule',
                'verbose_name_plural': 'Schedule',
                'ordering': ('-created_at',),
            },
        ),
    ]
