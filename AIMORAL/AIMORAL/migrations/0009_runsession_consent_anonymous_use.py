from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("AIMORAL", "0008_replace_age_with_age_group"),
    ]

    operations = [
        migrations.AddField(
            model_name="runsession",
            name="consent_anonymous_use",
            field=models.BooleanField(default=False),
        ),
    ]
