# Generated by Django 4.2.1 on 2023-05-18 02:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userincome', '0008_alter_source_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userincome',
            old_name='source',
            new_name='incomeSource',
        ),
    ]
