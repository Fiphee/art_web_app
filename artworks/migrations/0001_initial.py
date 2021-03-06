# Generated by Django 3.1.7 on 2021-03-20 16:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArtFavourite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArtLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Artwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='artworks/original_images')),
                ('thumbnail', models.ImageField(default='default_thumb.jpg', upload_to='artworks/thumbnails')),
                ('category', models.ManyToManyField(related_name='artworks', through='artworks.ArtCategory', to='artworks.Category')),
                ('favourites', models.ManyToManyField(related_name='favourite_artworks', through='artworks.ArtFavourite', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(related_name='artworks_liked', through='artworks.ArtLike', to=settings.AUTH_USER_MODEL)),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='artlike',
            name='art_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artworks.artwork'),
        ),
        migrations.AddField(
            model_name='artlike',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='artfavourite',
            name='art_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artworks.artwork'),
        ),
        migrations.AddField(
            model_name='artfavourite',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='artcategory',
            name='art_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artworks.artwork'),
        ),
        migrations.AddField(
            model_name='artcategory',
            name='category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artworks.category'),
        ),
    ]
