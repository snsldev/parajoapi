# Generated by Django 3.0.4 on 2020-03-26 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0003_auto_20200326_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carinfo',
            name='seq',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
