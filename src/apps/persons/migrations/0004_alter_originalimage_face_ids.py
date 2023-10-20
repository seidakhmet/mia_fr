# Generated by Django 4.2.2 on 2023-10-19 10:27

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("persons", "0003_alter_originalimage_face_ids"),
    ]

    operations = [
        migrations.AlterField(
            model_name="originalimage",
            name="face_ids",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(blank=True),
                blank=True,
                default=list,
                size=None,
                verbose_name="Face identities",
            ),
        ),
    ]
