# Generated by Django 3.1.3 on 2020-12-15 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concerts', '0004_auto_20201215_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concert',
            name='host',
            field=models.ManyToManyField(db_table='concerts_hosts', to='concerts.Host'),
        ),
    ]