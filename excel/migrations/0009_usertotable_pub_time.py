# Generated by Django 2.0.2 on 2018-03-16 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excel', '0008_auto_20180316_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertotable',
            name='pub_time',
            field=models.DateTimeField(null=True),
        ),
    ]
