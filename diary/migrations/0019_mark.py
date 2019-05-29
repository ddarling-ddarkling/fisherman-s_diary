# Generated by Django 2.2.1 on 2019-05-29 14:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('diary', '0018_auto_20190526_1743'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('like', 'нравится'), ('dislike', 'не нравится'), ('neutral', 'нейтральная')], default='neutral', max_length=12)),
                ('diary_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diary.Diary')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]