from django.test import TestCase
from django.urls import reverse

from .models import RunSession, Scenario


class EthicalProfilingFlowTests(TestCase):
    def setUp(self):
        Scenario.objects.exclude(question_code__in=[1, 2]).update(is_active=False)
        Scenario.objects.filter(question_code__in=[1, 2]).update(is_active=True)

    def test_completed_run_renders_new_profile_sections(self):
        start_response = self.client.post(
            reverse("aimoral:start"),
            {
                "age_group": "25-45",
                "gender": "female",
                "consent_anonymous_use": "on",
            },
        )
        self.assertRedirects(start_response, reverse("aimoral:question", args=[1]))
        run = RunSession.objects.latest("id")
        self.assertEqual(run.age_group, "25-45")
        self.assertEqual(run.gender, "female")
        self.assertTrue(run.consent_anonymous_use)

        first = self.client.post(reverse("aimoral:question", args=[1]), {"selected_side": "left"})
        self.assertRedirects(first, reverse("aimoral:question", args=[2]))

        response = self.client.post(
            reverse("aimoral:question", args=[2]),
            {"selected_side": "right"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ethical Dimensions")
        self.assertContains(response, "Moral Tensions")
        self.assertNotContains(response, "Moral Archetypes")
        self.assertNotContains(response, "Choice pattern")
        self.assertNotContains(response, "Baseline split")
        self.assertNotContains(response, "Lead signals")
        self.assertNotContains(response, "Scenario Alignment")
        self.assertEqual(len(response.context["score_scales"]), 5)
        self.assertEqual(len(response.context["tension_scales"]), 5)
        self.assertEqual(len(response.context["archetype_scales"]), 5)

    def test_start_requires_demographic_fields(self):
        response = self.client.post(
            reverse("aimoral:start"),
            {"age_group": "", "gender": "", "consent_anonymous_use": "on"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Please select your age range.", status_code=400)

    def test_start_rejects_invalid_gender(self):
        response = self.client.post(
            reverse("aimoral:start"),
            {
                "age_group": "25-45",
                "gender": "non-binary",
                "consent_anonymous_use": "on",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Please select a valid gender.", status_code=400)

    def test_start_rejects_invalid_age_group(self):
        response = self.client.post(
            reverse("aimoral:start"),
            {
                "age_group": "12-17",
                "gender": "male",
                "consent_anonymous_use": "on",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Please select a valid age range.", status_code=400)

    def test_start_accepts_other_gender(self):
        response = self.client.post(
            reverse("aimoral:start"),
            {
                "age_group": "25-45",
                "gender": "other",
                "consent_anonymous_use": "on",
            },
        )

        self.assertRedirects(response, reverse("aimoral:question", args=[1]))
        run = RunSession.objects.latest("id")
        self.assertEqual(run.gender, "other")

    def test_start_requires_anonymous_consent(self):
        response = self.client.post(
            reverse("aimoral:start"),
            {"age_group": "25-45", "gender": "male"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertContains(
            response,
            "Please accept anonymous use of your answers to continue.",
            status_code=400,
        )
