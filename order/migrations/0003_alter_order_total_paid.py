# Generated by Django 4.1.1 on 2022-10-29 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0002_rename_full_name_order_first_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="total_paid",
            field=models.CharField(max_length=20),
        ),
    ]