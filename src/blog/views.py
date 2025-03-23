from django.views.generic.base import TemplateView
from django.conf import settings

BASE_DIR = settings.BASE_DIR


class HomeView(TemplateView):
    template_name = str(BASE_DIR) + "/blog/templates/blog/landing.html"
