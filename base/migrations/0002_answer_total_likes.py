# Generated by Django 4.1.5 on 2023-07-23 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='total_likes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
