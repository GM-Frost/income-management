# Generated by Django 4.2.1 on 2023-05-18 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userincome', '0004_rename_income_userincome_alter_userincome_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='source',
            options={'verbose_name_plural': 'Source'},
        ),
        migrations.AlterModelOptions(
            name='userincome',
            options={},
        ),
        migrations.RenameField(
            model_name='userincome',
            old_name='source',
            new_name='src',
        ),
    ]
