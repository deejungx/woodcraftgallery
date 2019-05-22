from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
import datetime


class NewsIndexPage(Page):

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        new_posts = NewsPostPage.objects.live().public().order_by('-first_published_at')
        paginator = Paginator(new_posts, 6)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context["posts"] = posts
        return context


class NewsPostPage(Page):

    posttitle = models.CharField(max_length=250)
    subheading = models.CharField(max_length=250)
    body = RichTextField()
    featured_image = models.ForeignKey(
                    'wagtailimages.Image',
                    null=True,
                    blank=True,
                    on_delete=models.SET_NULL,
                    related_name='+'
    )
    featured_image_caption = models.CharField(max_length=250,
                                              null=True,
                                              blank=True
    )

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('subheading'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('posttitle'),
        FieldPanel('subheading'),
        FieldPanel('body', classname="full"),
        ImageChooserPanel('featured_image'),
        FieldPanel('featured_image_caption'),
    ]

    parent_page_types = ['news.NewsIndexPage']
