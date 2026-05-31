from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("AIMORAL", "0007_runsession_demographics"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="runsession",
            name="age",
        ),
        migrations.AddField(
            model_name="runsession",
            name="age_group",
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
