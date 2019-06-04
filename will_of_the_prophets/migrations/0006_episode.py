# Generated by Django 2.2 on 2019-05-24 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("will_of_the_prophets", "0005_timeframe_specialsquares_and_buttholes")
    ]

    operations = [
        migrations.CreateModel(
            name="Episode",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=256)),
                ("date", models.DateField()),
                ("itunes_id", models.SmallIntegerField(unique=True)),
            ],
        )
    ]
