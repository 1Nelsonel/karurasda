# Generated by Django 4.2.3 on 2023-08-20 08:29

from django.db import migrations, models
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_sermon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videolink', embed_video.fields.EmbedVideoField(default='https://www.youtube.com/embed/XFrjmhTyiYI')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-updated', '-created'],
            },
        ),
    ]
