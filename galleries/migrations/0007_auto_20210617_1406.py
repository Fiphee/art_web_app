# Generated by Django 3.1.7 on 2021-06-17 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('galleries', '0006_auto_20210414_2227'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gallery',
            options={'ordering': ['position'], 'verbose_name_plural': 'Galleries'},
        ),
    ]