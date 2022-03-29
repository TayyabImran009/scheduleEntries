# Generated by Django 4.0.1 on 2022-03-28 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='is_receptionest',
            new_name='is_dentist',
        ),
        migrations.AddField(
            model_name='account',
            name='is_nurse',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='account',
            name='is_reception',
            field=models.BooleanField(default=False),
        ),
    ]
