# Generated by Django 2.2.6 on 2019-10-27 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0002_component'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='component_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='component',
            name='component_sim',
            field=models.CharField(max_length=100),
        ),
    ]
