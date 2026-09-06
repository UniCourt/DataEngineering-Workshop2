from django.apps import AppConfig
from web_scrapper import start_extraction


class MembersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "members"

