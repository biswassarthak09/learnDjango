# Generated by Django 5.0 on 2023-12-27 10:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("travelo", "0005_remove_package_destination_package_description_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="package",
            old_name="description_id",
            new_name="destination_id",
        ),
    ]