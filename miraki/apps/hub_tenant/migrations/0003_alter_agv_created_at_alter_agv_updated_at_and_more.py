# Generated by Django 4.1.9 on 2023-07-31 15:12

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("hub_tenant", "0002_userprofile_onboarded_alter_agv_created_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="agv",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 7, 31, 20, 42, 19, 967128)),
        ),
        migrations.AlterField(
            model_name="agv",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 31, 20, 42, 19, 967168)),
        ),
        migrations.AlterField(
            model_name="area",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 7, 31, 20, 42, 20, 8145)),
        ),
        migrations.AlterField(
            model_name="area",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 31, 20, 42, 20, 8178)),
        ),
        migrations.AlterField(
            model_name="cnc",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 7, 31, 20, 42, 19, 967128)),
        ),
        migrations.AlterField(
            model_name="cnc",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 31, 20, 42, 19, 967168)),
        ),
        migrations.AlterField(
            model_name="connectioninfo",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 7, 31, 20, 42, 19, 967128)),
        ),
        migrations.AlterField(
            model_name="connectioninfo",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 31, 20, 42, 19, 967168)),
        ),
        migrations.AlterField(
            model_name="edgedevice",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 7, 31, 20, 42, 19, 967128)),
        ),
        migrations.AlterField(
            model_name="edgedevice",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 31, 20, 42, 19, 967168)),
        ),
        migrations.AlterField(
            model_name="line",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 7, 31, 20, 42, 20, 8145)),
        ),
        migrations.AlterField(
            model_name="line",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 31, 20, 42, 20, 8178)),
        ),
        migrations.AlterField(
            model_name="machine",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 7, 31, 20, 42, 20, 8145)),
        ),
        migrations.AlterField(
            model_name="machine",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 31, 20, 42, 20, 8178)),
        ),
        migrations.AlterField(
            model_name="plc",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 7, 31, 20, 42, 19, 967128)),
        ),
        migrations.AlterField(
            model_name="plc",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 31, 20, 42, 19, 967168)),
        ),
        migrations.AlterField(
            model_name="process",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 7, 31, 20, 42, 20, 8145)),
        ),
        migrations.AlterField(
            model_name="process",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 31, 20, 42, 20, 8178)),
        ),
        migrations.AlterField(
            model_name="robot",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 7, 31, 20, 42, 19, 967128)),
        ),
        migrations.AlterField(
            model_name="robot",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 31, 20, 42, 19, 967168)),
        ),
        migrations.AlterField(
            model_name="site",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 7, 31, 20, 42, 20, 8145)),
        ),
        migrations.AlterField(
            model_name="site",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 31, 20, 42, 20, 8178)),
        ),
        migrations.AlterField(
            model_name="tagtopics",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 7, 31, 20, 42, 20, 8145)),
        ),
        migrations.AlterField(
            model_name="tagtopics",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 31, 20, 42, 20, 8178)),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 7, 31, 20, 42, 19, 967128)),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 31, 20, 42, 19, 967168)),
        ),
        migrations.AlterField(
            model_name="vision",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 7, 31, 20, 42, 19, 967128)),
        ),
        migrations.AlterField(
            model_name="vision",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 31, 20, 42, 19, 967168)),
        ),
        migrations.CreateModel(
            name="Organization",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                (
                    "created_at",
                    models.DateTimeField(db_index=True, default=datetime.datetime(2023, 7, 31, 20, 42, 19, 967128)),
                ),
                ("updated_at", models.DateTimeField(default=datetime.datetime(2023, 7, 31, 20, 42, 19, 967168))),
                ("space_name", models.CharField(max_length=100)),
                ("org_name", models.CharField(max_length=500)),
                ("address", models.JSONField(default=dict)),
                ("org_img", models.ImageField(blank=True, null=True, upload_to="org_img")),
                (
                    "owners",
                    models.ManyToManyField(blank=True, related_name="%(class)s_owners", to="hub_tenant.userprofile"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MyDashboard",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                (
                    "created_at",
                    models.DateTimeField(db_index=True, default=datetime.datetime(2023, 7, 31, 20, 42, 19, 967128)),
                ),
                ("updated_at", models.DateTimeField(default=datetime.datetime(2023, 7, 31, 20, 42, 19, 967168))),
                ("name", models.CharField(max_length=100)),
                ("is_default", models.BooleanField(default=False)),
                ("widgets", models.JSONField(default=dict)),
                (
                    "created_by",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="hub_tenant.userprofile"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]