from django.db import models
from exhibition.models import ExhibitionDetailPage
from news.models import NewsPostPage

from wagtail.core.models import Page

def sortDate(elem):
     return elem.first_published_at

class HomePage(Page):

    def get_context(self, request):
        context = super().get_context(request)
        newspages = [x for x in NewsPostPage.objects.live().all()]
        exhibitionpages = [x for x in ExhibitionDetailPage.objects.live().all()]
        allpages = newspages + exhibitionpages
        featuredPages = sorted(allpages, key=sortDate, reverse=True)[:7]
        context['featured_pages'] = featuredPages
        return context


    class Meta:
        verbose_name = "homepage"
