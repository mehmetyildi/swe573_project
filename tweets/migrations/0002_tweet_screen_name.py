# Generated by Django 2.1.2 on 2018-11-19 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='screen_name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
