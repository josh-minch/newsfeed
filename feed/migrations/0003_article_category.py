# Generated by Django 2.2.7 on 2019-12-07 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_auto_20191128_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.CharField(default='general', max_length=200),
            preserve_default=False,
        ),
    ]