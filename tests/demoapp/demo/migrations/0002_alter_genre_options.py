# Generated by Django 4.0.2 on 2022-02-14 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='band',
            name='genre',
            field=models.IntegerField(blank=True, choices=[(1, 'Rock'), (2, 'Blues'), (3, 'Soul'), (4, 'Other')], null=True),
        )
    ]