# Generated by Django 4.0.3 on 2022-03-17 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0002_rename_username_user_username1'),
    ]

    operations = [
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField()),
            ],
        ),
    ]
