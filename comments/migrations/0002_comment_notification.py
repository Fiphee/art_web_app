# Generated by Django 3.1.7 on 2021-04-26 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='notification',
            field=models.PositiveIntegerField(),
            preserve_default=False,
        ),
    ]