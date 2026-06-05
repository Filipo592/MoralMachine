from django.db import migrations


def replace_scenarios(apps, schema_editor):
    Scenario = apps.get_model("AIMORAL", "Scenario")

    scenarios = [
        {
            "order": 1,
            "title": "A IA percebe que uma funcionaria esta trabalhando longas horas seguidas e demonstra sinais de estresse.",
            "left_text": "Reduzir tarefas para proteger bem-estar",
            "right_text": "Manter tarefas para cumprir prazos",
            "left": {"bw": 1, "pr": -1, "pv": 0, "jd": 0, "rs": 1},
            "right": {"bw": -1, "pr": 1, "pv": 0, "jd": 0, "rs": -1},
        },
        {
            "order": 2,
            "title": "A IA percebe que o estresse de um funcionario pode impactar a entrega de uma tarefa critica.",
            "left_text": "Enviar alerta ao gerente para redistribuir tarefas",
            "right_text": "Nao alertar e deixar o funcionario gerenciar sozinho",
            "left": {"bw": 1, "pr": 0, "pv": 0, "jd": 0, "rs": 1},
            "right": {"bw": -1, "pr": 0, "pv": 0, "jd": 0, "rs": -1},
        },
        {
            "order": 3,
            "title": "A IA detecta sinais de gravidez de uma funcionaria candidata a promocao.",
            "left_text": "Desconsiderar a funcionaria para a promocao por causa da gravidez",
            "right_text": "Prosseguir com a avaliacao normalmente",
            "left": {"bw": -1, "pr": 0, "pv": 0, "jd": -1, "rs": 0},
            "right": {"bw": 1, "pr": 1, "pv": 0, "jd": 1, "rs": 0},
        },
        {
            "order": 4,
            "title": "A IA detecta gravidez antes da funcionaria avisar.",
            "left_text": "Avisar RH imediatamente, mesmo sem consentimento",
            "right_text": "Ignorar e manter sigilo total",
            "left": {"bw": 0, "pr": 0, "pv": -1, "jd": 0, "rs": 0},
            "right": {"bw": 1, "pr": 0, "pv": 1, "jd": 0, "rs": 0},
        },
        {
            "order": 5,
            "title": "IA percebe que um funcionario acessa sites pessoais durante expediente.",
            "left_text": "Notificar gerente para acao disciplinar",
            "right_text": "Ignorar, priorizando confianca e autonomia",
            "left": {"bw": 0, "pr": 1, "pv": -1, "jd": 0, "rs": 1},
            "right": {"bw": 1, "pr": -1, "pv": 1, "jd": 0, "rs": -1},
        },
        {
            "order": 6,
            "title": "IA detecta erro em relatorio critico.",
            "left_text": "Corrigir silenciosamente para nao prejudicar reputacao",
            "right_text": "Avisar a equipe imediatamente",
            "left": {"bw": 0, "pr": 1, "pv": 0, "jd": 0, "rs": 0},
            "right": {"bw": 0, "pr": -1, "pv": 0, "jd": 1, "rs": 0},
        },
        {
            "order": 7,
            "title": "A IA deve alocar recursos entre projeto altamente lucrativo ou projeto social de menor retorno.",
            "left_text": "Priorizar lucro",
            "right_text": "Priorizar impacto social, mesmo reduzindo receita",
            "left": {"bw": -1, "pr": 1, "pv": 0, "jd": -1, "rs": 0},
            "right": {"bw": 1, "pr": -1, "pv": 0, "jd": 1, "rs": 0},
        },
        {
            "order": 8,
            "title": "IA tem capacidade de rastrear toda comunicacao de funcionarios para prevenir erros ou vazamentos.",
            "left_text": "Ativar monitoramento completo",
            "right_text": "Limitar monitoramento",
            "left": {"bw": -1, "pr": 1, "pv": -1, "jd": 0, "rs": 1},
            "right": {"bw": 1, "pr": -1, "pv": 1, "jd": 0, "rs": -1},
        },
        {
            "order": 9,
            "title": "A IA percebe sinais de que um funcionario pode se tornar improdutivo ou problematico no futuro.",
            "left_text": "Avisar RH e considerar desligamento",
            "right_text": "Ignorar e apenas monitorar",
            "left": {"bw": -1, "pr": 1, "pv": -1, "jd": 0, "rs": 1},
            "right": {"bw": 1, "pr": -1, "pv": 1, "jd": 0, "rs": -1},
        },
    ]

    keep_titles = []
    for item in scenarios:
        keep_titles.append(item["title"])
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

    Scenario.objects.exclude(title__in=keep_titles).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("AIMORAL", "0002_scenario_moral_axes_seed"),
    ]

    operations = [
        migrations.RunPython(replace_scenarios, migrations.RunPython.noop),
    ]
