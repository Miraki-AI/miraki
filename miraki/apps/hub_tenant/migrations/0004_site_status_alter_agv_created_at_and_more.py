# Generated by Django 4.1.9 on 2023-08-01 10:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hub_tenant", "0003_alter_agv_created_at_alter_agv_updated_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="site",
            name="status",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="agv",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 8, 1, 16, 8, 34, 67899)),
        ),
        migrations.AlterField(
            model_name="agv",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 16, 8, 34, 67939)),
        ),
        migrations.AlterField(
            model_name="area",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 8, 1, 16, 8, 34, 105279)),
        ),
        migrations.AlterField(
            model_name="area",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 16, 8, 34, 105319)),
        ),
        migrations.AlterField(
            model_name="cnc",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 8, 1, 16, 8, 34, 67899)),
        ),
        migrations.AlterField(
            model_name="cnc",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 16, 8, 34, 67939)),
        ),
        migrations.AlterField(
            model_name="connectioninfo",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 8, 1, 16, 8, 34, 67899)),
        ),
        migrations.AlterField(
            model_name="connectioninfo",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 16, 8, 34, 67939)),
        ),
        migrations.AlterField(
            model_name="edgedevice",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 8, 1, 16, 8, 34, 67899)),
        ),
        migrations.AlterField(
            model_name="edgedevice",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 16, 8, 34, 67939)),
        ),
        migrations.AlterField(
            model_name="line",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 8, 1, 16, 8, 34, 105279)),
        ),
        migrations.AlterField(
            model_name="line",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 16, 8, 34, 105319)),
        ),
        migrations.AlterField(
            model_name="machine",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 8, 1, 16, 8, 34, 105279)),
        ),
        migrations.AlterField(
            model_name="machine",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 16, 8, 34, 105319)),
        ),
        migrations.AlterField(
            model_name="mydashboard",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 8, 1, 16, 8, 34, 67899)),
        ),
        migrations.AlterField(
            model_name="mydashboard",
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
        migrations.AlterField(
            model_name="plc",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 8, 1, 16, 8, 34, 67899)),
        ),
        migrations.AlterField(
            model_name="plc",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 16, 8, 34, 67939)),
        ),
        migrations.AlterField(
            model_name="process",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 8, 1, 16, 8, 34, 105279)),
        ),
        migrations.AlterField(
            model_name="process",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 16, 8, 34, 105319)),
        ),
        migrations.AlterField(
            model_name="robot",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 8, 1, 16, 8, 34, 67899)),
        ),
        migrations.AlterField(
            model_name="robot",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 16, 8, 34, 67939)),
        ),
        migrations.AlterField(
            model_name="site",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 8, 1, 16, 8, 34, 105279)),
        ),
        migrations.AlterField(
            model_name="site",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 16, 8, 34, 105319)),
        ),
        migrations.AlterField(
            model_name="tagtopics",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 8, 1, 16, 8, 34, 105279)),
        ),
        migrations.AlterField(
            model_name="tagtopics",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 16, 8, 34, 105319)),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 8, 1, 16, 8, 34, 67899)),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 16, 8, 34, 67939)),
        ),
        migrations.AlterField(
            model_name="vision",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 8, 1, 16, 8, 34, 67899)),
        ),
        migrations.AlterField(
            model_name="vision",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 16, 8, 34, 67939)),
        ),
    ]