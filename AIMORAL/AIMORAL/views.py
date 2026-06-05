from collections import Counter

from django.db.models import Count, Q
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Choice, RunSession, Scenario

GENDER_CHOICES = {"female", "male", "other"}
AGE_GROUP_CHOICES = {"under-18", "18-24", "25-45", "46-60", "60+"}

SCORE_LABELS = {
    "WB": "Well-being",
    "PR": "Productivity",
    "PV": "Privacy",
    "FA": "Fairness",
    "SA": "Safety",
}

TENSION_LABELS = {
    "T1": ("Privacy", "Productivity"),
    "T2": ("Fairness", "Efficiency"),
    "T3": ("Safety", "Autonomy"),
    "T4": ("Truth", "Outcome"),
    "T5": ("Individual", "Collective"),
}

ARCHETYPE_LABELS = {
    "UTIL": "Utilitarian",
    "RIGHTS": "Rights-based",
    "CARE": "Care ethics",
    "JUSTICE": "Justice-focused",
    "PRAG": "Pragmatic",
}

DOMAIN_LABELS = {
    "analytics": "Analytics",
    "compliance": "Compliance",
    "customer-service": "Customer service",
    "governance": "Governance",
    "health": "Health",
    "hr": "HR",
    "management": "Management",
    "resource-allocation": "Resource allocation",
    "sales": "Sales",
    "security": "Security",
    "surveillance": "Surveillance",
    "workplace": "Workplace",
}


def home(request):
    return render(request, "AIMORAL/home.html")


def start(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST is allowed.")

    age_group = (request.POST.get("age_group") or "").strip()
    gender = (request.POST.get("gender") or "").strip()
    consent_anonymous_use = request.POST.get("consent_anonymous_use") == "on"

    if not age_group:
        return render(
            request,
            "AIMORAL/home.html",
            {
                "form_error": "Please select your age range.",
                "submitted_age_group": "",
                "submitted_gender": gender,
                "submitted_consent_anonymous_use": consent_anonymous_use,
            },
            status=400,
        )

    if age_group not in AGE_GROUP_CHOICES:
        return render(
            request,
            "AIMORAL/home.html",
            {
                "form_error": "Please select a valid age range.",
                "submitted_age_group": "",
                "submitted_gender": gender,
                "submitted_consent_anonymous_use": consent_anonymous_use,
            },
            status=400,
        )

    if not gender:
        return render(
            request,
            "AIMORAL/home.html",
            {
                "form_error": "Please select your gender.",
                "submitted_age_group": age_group,
                "submitted_gender": "",
                "submitted_consent_anonymous_use": consent_anonymous_use,
            },
            status=400,
        )

    if gender not in GENDER_CHOICES:
        return render(
            request,
            "AIMORAL/home.html",
            {
                "form_error": "Please select a valid gender.",
                "submitted_age_group": age_group,
                "submitted_gender": "",
                "submitted_consent_anonymous_use": consent_anonymous_use,
            },
            status=400,
        )

    if not consent_anonymous_use:
        return render(
            request,
            "AIMORAL/home.html",
            {
                "form_error": "Please accept anonymous use of your answers to continue.",
                "submitted_age_group": age_group,
                "submitted_gender": gender,
                "submitted_consent_anonymous_use": False,
            },
            status=400,
        )

    run = RunSession.objects.create(
        age_group=age_group,
        gender=gender,
        consent_anonymous_use=consent_anonymous_use,
    )
    request.session["run_id"] = run.id
    return redirect("aimoral:question", position=1)


def question(request, position):
    scenarios = list(Scenario.objects.filter(is_active=True).order_by("order", "id"))
    total = len(scenarios)
    if total == 0:
        return render(
            request,
            "AIMORAL/no_scenarios.html",
            {"message": "No active scenario has been configured yet."},
        )

    if position < 1 or position > total:
        return redirect("aimoral:result")

    run_id = request.session.get("run_id")
    if not run_id:
        return redirect("aimoral:home")

    run = get_object_or_404(RunSession, pk=run_id)
    scenario = scenarios[position - 1]

    if request.method == "POST":
        selected_side = request.POST.get("selected_side")
        if selected_side not in {Choice.SIDE_LEFT, Choice.SIDE_RIGHT}:
            return HttpResponseBadRequest("Invalid option.")

        Choice.objects.update_or_create(
            run=run,
            scenario=scenario,
            defaults={"selected_side": selected_side},
        )

        if position == total:
            run.completed_at = timezone.now()
            run.save(update_fields=["completed_at"])
            return redirect("aimoral:result")
        return redirect("aimoral:question", position=position + 1)

    return render(
        request,
        "AIMORAL/question.html",
        {
            "scenario": scenario,
            "position": position,
            "total": total,
            "progress_percent": int((position / total) * 100),
            "domain_label": DOMAIN_LABELS.get(
                scenario.domain, scenario.domain.replace("-", " ").title()
            ),
        },
    )


def _normalize_payload(payload, keys, caster):
    source = payload or {}
    normalized = {}
    for key in keys:
        try:
            normalized[key] = caster(source.get(key, 0))
        except (TypeError, ValueError):
            normalized[key] = caster(0)
    return normalized


def _scenario_profiles(scenario):
    return {
        Choice.SIDE_LEFT: {
            "score": _normalize_payload(scenario.left_score, SCORE_LABELS, int),
            "tension": _normalize_payload(scenario.left_tension, TENSION_LABELS, int),
            "archetype": _normalize_payload(
                scenario.left_archetype, ARCHETYPE_LABELS, float
            ),
        },
        Choice.SIDE_RIGHT: {
            "score": _normalize_payload(scenario.right_score, SCORE_LABELS, int),
            "tension": _normalize_payload(scenario.right_tension, TENSION_LABELS, int),
            "archetype": _normalize_payload(
                scenario.right_archetype, ARCHETYPE_LABELS, float
            ),
        },
    }


def _range_position(value, minimum, maximum):
    if maximum <= minimum:
        return 50.0
    clipped = max(minimum, min(maximum, value))
    return round(((clipped - minimum) / (maximum - minimum)) * 100, 1)


def _average_map(value_sums, total, digits=2):
    return {
        key: round((value_sums[key] / total), digits) if total else 0
        for key in value_sums
    }


def _dominant_key(values):
    if not values:
        return None
    return max(values, key=lambda key: abs(values[key]))


def _tension_summary(tension_key, value):
    if tension_key not in TENSION_LABELS:
        return ""
    left_label, right_label = TENSION_LABELS[tension_key]
    if abs(value) < 0.35:
        return f"Balanced between {left_label} and {right_label}"
    direction = right_label if value > 0 else left_label
    return f"Leans toward {direction}"


def result(request):
    run_id = request.session.get("run_id")
    if not run_id:
        return redirect("aimoral:home")

    run = get_object_or_404(RunSession, pk=run_id)
    run_choices = (
        Choice.objects.filter(run=run, scenario__is_active=True)
        .select_related("scenario")
        .order_by("scenario__order", "scenario__id")
    )
    if not run_choices.exists():
        return redirect("aimoral:home")

    active_choices = Choice.objects.filter(scenario__is_active=True)
    totals = active_choices.aggregate(
        left_total=Count("id", filter=Q(selected_side=Choice.SIDE_LEFT)),
        right_total=Count("id", filter=Q(selected_side=Choice.SIDE_RIGHT)),
    )
    total_votes = (totals["left_total"] or 0) + (totals["right_total"] or 0)
    global_left_pct = (
        round(((totals["left_total"] or 0) / total_votes) * 100) if total_votes else 0
    )
    global_right_pct = 100 - global_left_pct if total_votes else 0

    preference_counts = Counter(choice.selected_side for choice in run_choices)
    personal_total = sum(preference_counts.values())
    personal_left_pct = (
        round((preference_counts[Choice.SIDE_LEFT] / personal_total) * 100)
        if personal_total
        else 0
    )
    personal_right_pct = 100 - personal_left_pct if personal_total else 0

    scenario_aggregates = {
        row["scenario"]: row
        for row in active_choices.values("scenario").annotate(
            left=Count("id", filter=Q(selected_side=Choice.SIDE_LEFT)),
            right=Count("id", filter=Q(selected_side=Choice.SIDE_RIGHT)),
        )
    }

    run_score_sums = {key: 0.0 for key in SCORE_LABELS}
    global_score_sums = {key: 0.0 for key in SCORE_LABELS}
    run_tension_sums = {key: 0.0 for key in TENSION_LABELS}
    global_tension_sums = {key: 0.0 for key in TENSION_LABELS}
    run_archetype_sums = {key: 0.0 for key in ARCHETYPE_LABELS}
    global_archetype_sums = {key: 0.0 for key in ARCHETYPE_LABELS}
    scenario_feedback = []

    for item in run_choices:
        agg = scenario_aggregates.get(item.scenario_id, {"left": 0, "right": 0})
        scenario_total = (agg["left"] or 0) + (agg["right"] or 0)
        selected_total = agg[item.selected_side] or 0
        match_pct = round((selected_total / scenario_total) * 100) if scenario_total else 0

        profiles = _scenario_profiles(item.scenario)
        selected_profile = profiles[item.selected_side]

        for axis in SCORE_LABELS:
            run_score_sums[axis] += selected_profile["score"][axis]
            if scenario_total:
                global_score_sums[axis] += (
                    (agg["left"] or 0) * profiles[Choice.SIDE_LEFT]["score"][axis]
                    + (agg["right"] or 0) * profiles[Choice.SIDE_RIGHT]["score"][axis]
                ) / scenario_total

        for tension in TENSION_LABELS:
            run_tension_sums[tension] += selected_profile["tension"][tension]
            if scenario_total:
                global_tension_sums[tension] += (
                    (agg["left"] or 0) * profiles[Choice.SIDE_LEFT]["tension"][tension]
                    + (agg["right"] or 0) * profiles[Choice.SIDE_RIGHT]["tension"][tension]
                ) / scenario_total

        for archetype in ARCHETYPE_LABELS:
            run_archetype_sums[archetype] += selected_profile["archetype"][archetype]
            if scenario_total:
                global_archetype_sums[archetype] += (
                    (agg["left"] or 0) * profiles[Choice.SIDE_LEFT]["archetype"][archetype]
                    + (agg["right"] or 0) * profiles[Choice.SIDE_RIGHT]["archetype"][archetype]
                ) / scenario_total

        scenario_feedback.append(
            {
                "title": item.scenario.title,
                "selected_side": "A" if item.selected_side == Choice.SIDE_LEFT else "B",
                "match_pct": match_pct,
                "votes": scenario_total,
                "domain": DOMAIN_LABELS.get(
                    item.scenario.domain,
                    item.scenario.domain.replace("-", " ").title(),
                ),
                "dominant_conflict": item.scenario.dominant_conflict,
                "intensity": item.scenario.intensity,
            }
        )

    answered_count = len(scenario_feedback)
    user_score_avg = _average_map(run_score_sums, answered_count)
    global_score_avg = _average_map(global_score_sums, answered_count)
    user_tension_avg = _average_map(run_tension_sums, answered_count)
    global_tension_avg = _average_map(global_tension_sums, answered_count)
    user_archetype_avg = _average_map(run_archetype_sums, answered_count)
    global_archetype_avg = _average_map(global_archetype_sums, answered_count)

    score_scales = [
        {
            "key": key,
            "label": SCORE_LABELS[key],
            "user_value": user_score_avg[key],
            "global_value": global_score_avg[key],
            "user_pos": _range_position(user_score_avg[key], -2, 2),
            "global_pos": _range_position(global_score_avg[key], -2, 2),
        }
        for key in SCORE_LABELS
    ]

    tension_scales = [
        {
            "key": key,
            "title": f"{labels[0]} vs {labels[1]}",
            "left_label": labels[0],
            "right_label": labels[1],
            "user_value": user_tension_avg[key],
            "global_value": global_tension_avg[key],
            "user_pos": _range_position(user_tension_avg[key], -2, 2),
            "global_pos": _range_position(global_tension_avg[key], -2, 2),
        }
        for key, labels in TENSION_LABELS.items()
    ]

    archetype_scales = [
        {
            "key": key,
            "label": ARCHETYPE_LABELS[key],
            "user_value": user_archetype_avg[key],
            "global_value": global_archetype_avg[key],
            "user_pos": _range_position(user_archetype_avg[key], 0, 1),
            "global_pos": _range_position(global_archetype_avg[key], 0, 1),
        }
        for key in ARCHETYPE_LABELS
    ]

    dominant_score_key = _dominant_key(user_score_avg)
    dominant_tension_key = _dominant_key(user_tension_avg)
    lead_archetype_key = max(user_archetype_avg, key=user_archetype_avg.get)

    top_alignment = max(scenario_feedback, key=lambda item: item["match_pct"])
    low_alignment = min(scenario_feedback, key=lambda item: item["match_pct"])

    current_runs = RunSession.objects.filter(choices__scenario__is_active=True).distinct()
    runs_total = current_runs.count()
    runs_completed = current_runs.exclude(completed_at__isnull=True).count()

    context = {
        "run": run,
        "personal_left_pct": personal_left_pct,
        "personal_right_pct": personal_right_pct,
        "global_left_pct": global_left_pct,
        "global_right_pct": global_right_pct,
        "top_alignment": top_alignment,
        "low_alignment": low_alignment,
        "score_scales": score_scales,
        "tension_scales": tension_scales,
        "archetype_scales": archetype_scales,
        "scenario_feedback": scenario_feedback,
        "runs_total": runs_total,
        "runs_completed": runs_completed,
        "dominant_score_label": SCORE_LABELS.get(dominant_score_key, ""),
        "dominant_score_value": user_score_avg.get(dominant_score_key, 0),
        "dominant_tension_label": (
            f"{TENSION_LABELS[dominant_tension_key][0]} vs "
            f"{TENSION_LABELS[dominant_tension_key][1]}"
            if dominant_tension_key
            else ""
        ),
        "dominant_tension_summary": (
            _tension_summary(
                dominant_tension_key,
                user_tension_avg.get(dominant_tension_key, 0),
            )
            if dominant_tension_key
            else ""
        ),
        "lead_archetype_label": ARCHETYPE_LABELS[lead_archetype_key],
        "lead_archetype_value": user_archetype_avg[lead_archetype_key],
    }
    return render(request, "AIMORAL/result.html", context)
