# Generated by Django 4.1.9 on 2023-06-14 09:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hub_tenant", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="alarm",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574046)),
        ),
        migrations.AlterField(
            model_name="alarm",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574145)),
        ),
        migrations.AlterField(
            model_name="area",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574046)),
        ),
        migrations.AlterField(
            model_name="area",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574145)),
        ),
        migrations.AlterField(
            model_name="controlmodule",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574046)),
        ),
        migrations.AlterField(
            model_name="controlmodule",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574145)),
        ),
        migrations.AlterField(
            model_name="controlsystem",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574046)),
        ),
        migrations.AlterField(
            model_name="controlsystem",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574145)),
        ),
        migrations.AlterField(
            model_name="datapoint",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574046)),
        ),
        migrations.AlterField(
            model_name="datapoint",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574145)),
        ),
        migrations.AlterField(
            model_name="equipment",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574046)),
        ),
        migrations.AlterField(
            model_name="equipment",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574145)),
        ),
        migrations.AlterField(
            model_name="event",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574046)),
        ),
        migrations.AlterField(
            model_name="event",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574145)),
        ),
        migrations.AlterField(
            model_name="manufacturingfacility",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574046)),
        ),
        migrations.AlterField(
            model_name="manufacturingfacility",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574145)),
        ),
        migrations.AlterField(
            model_name="order",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574046)),
        ),
        migrations.AlterField(
            model_name="order",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574145)),
        ),
        migrations.AlterField(
            model_name="processdata",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574046)),
        ),
        migrations.AlterField(
            model_name="processdata",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574145)),
        ),
        migrations.AlterField(
            model_name="productionschedule",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574046)),
        ),
        migrations.AlterField(
            model_name="productionschedule",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574145)),
        ),
        migrations.AlterField(
            model_name="site",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574046)),
        ),
        migrations.AlterField(
            model_name="site",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574145)),
        ),
        migrations.AlterField(
            model_name="unit",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574046)),
        ),
        migrations.AlterField(
            model_name="unit",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574145)),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574046)),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 14, 14, 56, 30, 574145)),
        ),
    ]