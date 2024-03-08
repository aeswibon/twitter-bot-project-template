from django.urls import path
from django.urls.conf import include
from rest_framework.routers import SimpleRouter

from project_name.bot.api.viewset import BotViewset

router = SimpleRouter()
router.register("bot", BotViewset)

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
]
