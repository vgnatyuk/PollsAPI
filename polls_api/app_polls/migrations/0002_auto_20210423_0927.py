# Generated by Django 2.2 on 2021-04-23 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
