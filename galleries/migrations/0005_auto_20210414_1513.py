# Generated by Django 3.1.7 on 2021-04-14 13:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('galleries', '0004_auto_20210414_1511'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFollowedGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('position', models.IntegerField(default=0)),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='galleries.gallery')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.DeleteModel(
            name='UserSavedGallery',
        ),
        migrations.AlterField(
            model_name='gallery',
            name='users',
            field=models.ManyToManyField(related_name='followed_galleries', through='galleries.UserFollowedGallery', to=settings.AUTH_USER_MODEL),
        ),
    ]