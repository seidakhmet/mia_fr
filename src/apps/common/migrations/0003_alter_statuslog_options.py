# Generated by Django 4.2.2 on 2023-09-08 16:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0002_statuslog_username"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="statuslog",
            options={
                "ordering": ("-create_datetime",),
                "verbose_name": "Request log",
                "verbose_name_plural": "Request logs",
            },
        ),
    ]
