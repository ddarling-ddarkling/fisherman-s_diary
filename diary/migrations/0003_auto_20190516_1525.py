# Generated by Django 2.2.1 on 2019-05-16 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0002_diary_feeding_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='feeding_type',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
