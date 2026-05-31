from django.urls import path

from . import views

app_name = "aimoral"

urlpatterns = [
    path("", views.home, name="home"),
    path("start/", views.start, name="start"),
    path("question/<int:position>/", views.question, name="question"),
    path("result/", views.result, name="result"),
]
