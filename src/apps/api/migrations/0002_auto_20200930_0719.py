# Generated by Django 3.1 on 2020-09-30 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grhierarchy',
            old_name='group_id',
            new_name='group',
        ),
        migrations.RenameField(
            model_name='grhierarchy',
            old_name='mineral_id',
            new_name='mineral',
        ),
        migrations.RenameField(
            model_name='grhierarchy',
            old_name='root_id',
            new_name='root',
        ),
        migrations.RenameField(
            model_name='grhierarchy',
            old_name='serie_id',
            new_name='serie',
        ),
        migrations.RenameField(
            model_name='grhierarchy',
            old_name='subgroup_id',
            new_name='subgroup',
        ),
        migrations.RenameField(
            model_name='grhierarchy',
            old_name='supergroup_id',
            new_name='supergroup',
        ),
    ]