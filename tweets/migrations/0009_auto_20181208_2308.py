# Generated by Django 2.1.2 on 2018-12-08 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0008_reply'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reported',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_id', models.CharField(blank=True, max_length=250, null=True)),
                ('report_reason', models.CharField(blank=True, max_length=250, null=True)),
                ('tweet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reported_tweet', to='tweets.Tweet')),
            ],
        ),
        migrations.AlterField(
            model_name='reply',
            name='tweet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='threaded_reply', to='tweets.Tweet'),
        ),
    ]
