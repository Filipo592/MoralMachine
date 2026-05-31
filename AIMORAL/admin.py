from django.contrib import admin

from .models import Choice, RunSession, Scenario


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = (
        "question_code",
        "title",
        "domain",
        "dominant_conflict",
        "intensity",
        "order",
        "is_active",
    )
    list_editable = ("order", "is_active", "intensity")
    list_filter = ("domain", "dominant_conflict", "is_active")
    search_fields = ("title", "left_text", "right_text")


@admin.register(RunSession)
class RunSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "completed_at")
    ordering = ("-created_at",)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "run", "scenario", "selected_side", "created_at")
    list_filter = ("selected_side", "scenario")
    ordering = ("-created_at",)
