from django.db import models


class Scenario(models.Model):
    question_code = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        unique=True,
    )
    title = models.CharField(max_length=255)
    left_text = models.TextField()
    right_text = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    domain = models.CharField(max_length=40, default="workplace")
    dominant_conflict = models.CharField(max_length=2, default="T1")
    intensity = models.PositiveSmallIntegerField(default=1)
    left_score = models.JSONField(default=dict)
    right_score = models.JSONField(default=dict)
    left_tension = models.JSONField(default=dict)
    right_tension = models.JSONField(default=dict)
    left_archetype = models.JSONField(default=dict)
    right_archetype = models.JSONField(default=dict)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class RunSession(models.Model):
    age_group = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=30, blank=True)
    consent_anonymous_use = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"RunSession #{self.pk}"


class Choice(models.Model):
    SIDE_LEFT = "left"
    SIDE_RIGHT = "right"

    SIDE_CHOICES = [
        (SIDE_LEFT, "Left"),
        (SIDE_RIGHT, "Right"),
    ]

    run = models.ForeignKey(
        RunSession,
        on_delete=models.CASCADE,
        related_name="choices",
    )
    scenario = models.ForeignKey(
        Scenario,
        on_delete=models.CASCADE,
        related_name="choices",
    )
    selected_side = models.CharField(max_length=5, choices=SIDE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("run", "scenario")

    def __str__(self):
        return f"Run {self.run_id} - Scenario {self.scenario_id}: {self.selected_side}"
