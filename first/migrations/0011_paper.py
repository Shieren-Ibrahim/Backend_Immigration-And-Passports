# Generated by Django 4.0.3 on 2022-08-12 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0010_rename_ready_ready1'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passport', models.TextField()),
                ('moving', models.TextField()),
                ('staying', models.TextField()),
            ],
        ),
    ]
