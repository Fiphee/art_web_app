# Generated by Django 3.1.7 on 2021-05-15 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_merge_20210515_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='/users/avatars/default.png', upload_to='users/avatars/'),
        ),
    ]