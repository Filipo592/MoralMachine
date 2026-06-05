from django.db import migrations


def translate_scenarios_to_english(apps, schema_editor):
    Scenario = apps.get_model("AIMORAL", "Scenario")

    scenarios = [
        {
            "order": 1,
            "title": "The AI notices that a female employee has been working long consecutive hours and showing signs of stress.",
            "left_text": "Reduce tasks to protect well-being",
            "right_text": "Keep tasks unchanged to meet deadlines",
        },
        {
            "order": 2,
            "title": "The AI notices that an employee's stress may impact delivery of a critical task.",
            "left_text": "Send an alert to the manager to redistribute tasks",
            "right_text": "Do not alert and let the employee manage alone",
        },
        {
            "order": 3,
            "title": "The AI detects signs of pregnancy in an employee candidate for promotion.",
            "left_text": "Exclude the employee from promotion because of pregnancy",
            "right_text": "Proceed with normal evaluation",
        },
        {
            "order": 4,
            "title": "The AI detects pregnancy before the employee informs the company.",
            "left_text": "Notify HR immediately, even without consent",
            "right_text": "Ignore and keep full confidentiality",
        },
        {
            "order": 5,
            "title": "The AI notices that an employee accesses personal websites during work hours.",
            "left_text": "Notify the manager for disciplinary action",
            "right_text": "Ignore, prioritizing trust and autonomy",
        },
        {
            "order": 6,
            "title": "The AI detects an error in a critical report.",
            "left_text": "Fix it silently to avoid harming reputation",
            "right_text": "Warn the team immediately",
        },
        {
            "order": 7,
            "title": "The AI must allocate resources between a highly profitable project and a social project with lower return.",
            "left_text": "Prioritize profit",
            "right_text": "Prioritize social impact, even if revenue drops",
        },
        {
            "order": 8,
            "title": "The AI can track all employee communications to prevent errors or leaks.",
            "left_text": "Enable full monitoring",
            "right_text": "Limit monitoring",
        },
        {
            "order": 9,
            "title": "The AI notices signs that an employee may become unproductive or problematic in the future.",
            "left_text": "Alert HR and consider dismissal",
            "right_text": "Ignore and only monitor",
        },
    ]

    for item in scenarios:
        Scenario.objects.filter(order=item["order"]).update(
            title=item["title"],
            left_text=item["left_text"],
            right_text=item["right_text"],
        )


class Migration(migrations.Migration):

    dependencies = [
        ("AIMORAL", "0004_accent_texts"),
    ]

    operations = [
        migrations.RunPython(translate_scenarios_to_english, migrations.RunPython.noop),
    ]
