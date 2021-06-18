# Generated by Django 3.1.7 on 2021-06-17 12:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artworks', '0007_auto_20210522_1815'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterField(
            model_name='artcolor',
            name='art',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='art_colors', to='artworks.artwork'),
        ),
        migrations.AlterField(
            model_name='artcolor',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='color_artworks', to='artworks.color'),
        ),
        migrations.AlterField(
            model_name='artwork',
            name='colors',
            field=models.ManyToManyField(blank=True, related_name='artworks', through='artworks.ArtColor', to='artworks.Color'),
        ),
        migrations.CreateModel(
            name='ArtDislike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('art', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artworks.artwork')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='artwork',
            name='dislikes',
            field=models.ManyToManyField(related_name='artworks_disliked', through='artworks.ArtDislike', to=settings.AUTH_USER_MODEL),
        ),
    ]
