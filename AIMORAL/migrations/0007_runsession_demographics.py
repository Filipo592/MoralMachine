from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("AIMORAL", "0006_ethical_profiling_engine"),
    ]

    operations = [
        migrations.AddField(
            model_name="runsession",
            name="age",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="runsession",
            name="gender",
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
