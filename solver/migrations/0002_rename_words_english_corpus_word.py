# Generated by Django 3.2.4 on 2022-02-01 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solver', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='english_corpus',
            old_name='words',
            new_name='word',
        ),
    ]
