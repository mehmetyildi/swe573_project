# Generated by Django 2.1.2 on 2018-11-27 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0005_auto_20181127_0048'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='stamp',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
