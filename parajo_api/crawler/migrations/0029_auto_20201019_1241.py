# Generated by Django 3.0.4 on 2020-10-19 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0028_auto_20201019_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carinfo',
            name='regdate',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
