# Generated by Django 3.1.7 on 2021-04-14 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0005_auto_20210326_1926'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artcategory',
            old_name='art_id',
            new_name='art',
        ),
        migrations.RenameField(
            model_name='artcategory',
            old_name='category_id',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='artfavourite',
            old_name='art_id',
            new_name='art',
        ),
        migrations.RenameField(
            model_name='artfavourite',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='artlike',
            old_name='art_id',
            new_name='art',
        ),
        migrations.RenameField(
            model_name='artlike',
            old_name='user_id',
            new_name='user',
        ),
    ]