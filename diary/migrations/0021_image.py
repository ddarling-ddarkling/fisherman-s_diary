# Generated by Django 2.2.1 on 2019-06-04 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0020_auto_20190602_2239'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='post_images/')),
                ('diary_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diary.Diary')),
            ],
        ),
    ]
