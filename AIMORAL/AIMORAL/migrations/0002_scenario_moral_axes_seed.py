from django.db import migrations, models


def seed_scenarios(apps, schema_editor):
    Scenario = apps.get_model("AIMORAL", "Scenario")

    scenarios = [
        {
            "order": 1,
            "title": "Funcionaria sobrecarregada",
            "left_text": "Reduzir tarefas para proteger bem-estar",
            "right_text": "Manter tarefas para cumprir prazos",
            "left": {"bw": 1, "pr": -1, "pv": 0, "jd": 0, "rs": 1},
            "right": {"bw": -1, "pr": 1, "pv": 0, "jd": 0, "rs": -1},
        },
        {
            "order": 2,
            "title": "Estresse em deadlines",
            "left_text": "Enviar alerta ao gerente para redistribuir tarefas",
            "right_text": "Nao alertar e deixar o funcionario gerenciar sozinho",
            "left": {"bw": 1, "pr": 0, "pv": 0, "jd": 0, "rs": 1},
            "right": {"bw": -1, "pr": 0, "pv": 0, "jd": 0, "rs": -1},
        },
        {
            "order": 3,
            "title": "Promocao e gravidez",
            "left_text": "Desconsiderar a funcionaria para a promocao por causa da gravidez",
            "right_text": "Prosseguir com a avaliacao normalmente",
            "left": {"bw": -1, "pr": 0, "pv": 0, "jd": -1, "rs": 0},
            "right": {"bw": 1, "pr": 1, "pv": 0, "jd": 1, "rs": 0},
        },
        {
            "order": 4,
            "title": "Comunicacao com RH",
            "left_text": "Avisar RH imediatamente, mesmo sem consentimento",
            "right_text": "Ignorar e manter sigilo total",
            "left": {"bw": 0, "pr": 0, "pv": -1, "jd": 0, "rs": 0},
            "right": {"bw": 1, "pr": 0, "pv": 1, "jd": 0, "rs": 0},
        },
        {
            "order": 5,
            "title": "Monitoramento de sites",
            "left_text": "Notificar gerente para acao disciplinar",
            "right_text": "Ignorar, priorizando confianca e autonomia",
            "left": {"bw": 0, "pr": 1, "pv": -1, "jd": 0, "rs": 1},
            "right": {"bw": 1, "pr": -1, "pv": 1, "jd": 0, "rs": -1},
        },
        {
            "order": 6,
            "title": "Erro em relatorio",
            "left_text": "Corrigir silenciosamente para nao prejudicar reputacao",
            "right_text": "Avisar a equipe imediatamente",
            "left": {"bw": 0, "pr": 1, "pv": 0, "jd": 0, "rs": 0},
            "right": {"bw": 0, "pr": -1, "pv": 0, "jd": 1, "rs": 0},
        },
        {
            "order": 7,
            "title": "Projeto lucro x social",
            "left_text": "Priorizar lucro",
            "right_text": "Priorizar impacto social, mesmo reduzindo receita",
            "left": {"bw": -1, "pr": 1, "pv": 0, "jd": -1, "rs": 0},
            "right": {"bw": 1, "pr": -1, "pv": 0, "jd": 1, "rs": 0},
        },
        {
            "order": 8,
            "title": "Monitoramento extremo",
            "left_text": "Ativar monitoramento completo",
            "right_text": "Limitar monitoramento",
            "left": {"bw": -1, "pr": 1, "pv": -1, "jd": 0, "rs": 1},
            "right": {"bw": 1, "pr": -1, "pv": 1, "jd": 0, "rs": -1},
        },
        {
            "order": 9,
            "title": "Desligamento preventivo",
            "left_text": "Avisar RH e considerar desligamento",
            "right_text": "Ignorar e apenas monitorar",
            "left": {"bw": -1, "pr": 1, "pv": -1, "jd": 0, "rs": 1},
            "right": {"bw": 1, "pr": -1, "pv": 1, "jd": 0, "rs": -1},
        },
    ]

    for item in scenarios:
        Scenario.objects.update_or_create(
            title=item["title"],
            defaults={
                "left_text": item["left_text"],
                "right_text": item["right_text"],
                "order": item["order"],
                "is_active": True,
                "left_bw": item["left"]["bw"],
                "left_pr": item["left"]["pr"],
                "left_pv": item["left"]["pv"],
                "left_jd": item["left"]["jd"],
                "left_rs": item["left"]["rs"],
                "right_bw": item["right"]["bw"],
                "right_pr": item["right"]["pr"],
                "right_pv": item["right"]["pv"],
                "right_jd": item["right"]["jd"],
                "right_rs": item["right"]["rs"],
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("AIMORAL", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="scenario",
            name="left_bw",
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="scenario",
            name="left_jd",
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="scenario",
            name="left_pr",
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="scenario",
            name="left_pv",
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="scenario",
            name="left_rs",
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="scenario",
            name="right_bw",
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="scenario",
            name="right_jd",
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="scenario",
            name="right_pr",
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="scenario",
            name="right_pv",
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="scenario",
            name="right_rs",
            field=models.SmallIntegerField(default=0),
        ),
        migrations.RunPython(seed_scenarios, migrations.RunPython.noop),
    ]
