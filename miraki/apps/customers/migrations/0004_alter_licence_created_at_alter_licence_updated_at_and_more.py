# Generated by Django 4.1.9 on 2023-08-01 10:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0003_alter_licence_created_at_alter_licence_updated_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="licence",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 8, 1, 16, 8, 34, 67899)),
        ),
        migrations.AlterField(
            model_name="licence",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 16, 8, 34, 67939)),
        ),
        migrations.AlterField(
            model_name="organization",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 8, 1, 16, 8, 34, 67899)),
        ),
        migrations.AlterField(
            model_name="organization",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 16, 8, 34, 67939)),
        ),
    ]