# Generated by Django 3.1.7 on 2021-04-07 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210327_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='/users/avatars/default.png', upload_to='users/avatars/'),
        ),
    ]
