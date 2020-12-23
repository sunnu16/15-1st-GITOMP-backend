# Generated by Django 3.1.4 on 2020-12-18 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='cd_image_url',
            field=models.URLField(default='/static/img/default_cd.jpg', max_length=256),
        ),
        migrations.AlterField(
            model_name='album',
            name='release_date',
            field=models.DateField(),
        ),
    ]
