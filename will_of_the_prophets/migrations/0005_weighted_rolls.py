# Generated by Django 2.1.4 on 2018-12-21 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("will_of_the_prophets", "0004_specialsquaretype_auto_move")
    ]

    operations = [
        migrations.AddField(
            model_name="specialsquaretype",
            name="weight",
            field=models.FloatField(
                default=1.0,
                help_text=(
                    "Relative likelihood of being landed on. If greater than one it's more likely, and if less than one it's less likely.",
                ),
            ),
        ),
        migrations.AlterField(
            model_name="roll",
            name="number",
            field=models.PositiveIntegerField(),
        ),
    ]
