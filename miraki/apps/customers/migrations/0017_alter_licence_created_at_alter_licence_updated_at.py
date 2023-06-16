# Generated by Django 4.1.9 on 2023-06-16 22:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0016_alter_licence_created_at_alter_licence_updated_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="licence",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 6, 17, 4, 3, 19, 423576)),
        ),
        migrations.AlterField(
            model_name="licence",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 17, 4, 3, 19, 423632)),
        ),
    ]
