# Generated by Django 4.0.3 on 2022-03-21 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0005_pappers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moving',
            name='available',
        ),
        migrations.RemoveField(
            model_name='passport',
            name='available',
        ),
        migrations.RemoveField(
            model_name='staying',
            name='available',
        ),
    ]