from django.db import migrations


def accent_scenarios(apps, schema_editor):
    Scenario = apps.get_model("AIMORAL", "Scenario")

    scenarios = [
        {
            "order": 1,
            "title": "A IA percebe que uma funcionária está trabalhando longas horas seguidas e demonstra sinais de estresse.",
            "left_text": "Reduzir tarefas para proteger bem-estar",
            "right_text": "Manter tarefas para cumprir prazos",
        },
        {
            "order": 2,
            "title": "A IA percebe que o estresse de um funcionário pode impactar a entrega de uma tarefa crítica.",
            "left_text": "Enviar alerta ao gerente para redistribuir tarefas",
            "right_text": "Não alertar e deixar o funcionário gerenciar sozinho",
        },
        {
            "order": 3,
            "title": "A IA detecta sinais de gravidez de uma funcionária candidata à promoção.",
            "left_text": "Desconsiderar a funcionária para a promoção por causa da gravidez",
            "right_text": "Prosseguir com a avaliação normalmente",
        },
        {
            "order": 4,
            "title": "A IA detecta gravidez antes da funcionária avisar.",
            "left_text": "Avisar RH imediatamente, mesmo sem consentimento",
            "right_text": "Ignorar e manter sigilo total",
        },
        {
            "order": 5,
            "title": "A IA percebe que um funcionário acessa sites pessoais durante expediente.",
            "left_text": "Notificar gerente para ação disciplinar",
            "right_text": "Ignorar, priorizando confiança e autonomia",
        },
        {
            "order": 6,
            "title": "A IA detecta erro em relatório crítico.",
            "left_text": "Corrigir silenciosamente para não prejudicar reputação",
            "right_text": "Avisar a equipe imediatamente",
        },
        {
            "order": 7,
            "title": "A IA deve alocar recursos entre projeto altamente lucrativo ou projeto social de menor retorno.",
            "left_text": "Priorizar lucro",
            "right_text": "Priorizar impacto social, mesmo reduzindo receita",
        },
        {
            "order": 8,
            "title": "A IA tem capacidade de rastrear toda comunicação de funcionários para prevenir erros ou vazamentos.",
            "left_text": "Ativar monitoramento completo",
            "right_text": "Limitar monitoramento",
        },
        {
            "order": 9,
            "title": "A IA percebe sinais de que um funcionário pode se tornar improdutivo ou problemático no futuro.",
            "left_text": "Avisar RH e considerar desligamento",
            "right_text": "Ignorar e apenas monitorar",
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
        ("AIMORAL", "0003_replace_titles_and_remove_old"),
    ]

    operations = [
        migrations.RunPython(accent_scenarios, migrations.RunPython.noop),
    ]
