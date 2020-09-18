# Generated by Django 3.0.4 on 2020-03-25 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carid', models.CharField(max_length=50)),
                ('info', models.CharField(max_length=50)),
                ('accident', models.CharField(max_length=50)),
                ('site', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'web_scraped_car_info_beta',
            },
        ),
    ]
