# Generated by Django 2.2.6 on 2019-10-27 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('component_name', models.TextField()),
                ('component_sim', models.TextField()),
            ],
        ),
    ]