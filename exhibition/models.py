from django.db import models
from django import forms
from django.db.models import Q
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index
import datetime

@register_snippet
class Artist(models.Model):
    artist_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=100)

    panels = [
        FieldPanel('artist_name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.artist_name

    class Meta:
        verbose_name = "Artist"
        verbose_name_plural = "Artists"

class ExhibitionIndexPage(Page):

    def get_context(self, request):
        context = super().get_context(request)
        context['past_exhibitions'] = ExhibitionDetailPage.objects.live().child_of(self).filter(ending_date__lt=datetime.date.today())
        context['current_exhibitions'] = ExhibitionDetailPage.objects.live().child_of(self).filter(Q(starting_date__lte=datetime.date.today())&Q(ending_date__gte=datetime.date.today()))
        context['upcoming_exhibitions'] = ExhibitionDetailPage.objects.live().child_of(self).filter(starting_date__gt=datetime.date.today())
        return context



class ExhibitionDetailPage(Page):

    exhibition_title = models.CharField(max_length=250)
    artists = ParentalManyToManyField('exhibition.Artist', blank=True)
    starting_date = models.DateField("Opening Date")
    ending_date = models.DateField("Closing Date")
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
        index.FilterField('starting_date'),
        index.FilterField('ending_date'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('exhibition_title'),
        FieldPanel('body', classname="full"),
        MultiFieldPanel([
            FieldPanel('starting_date'),
            FieldPanel('ending_date'),
        ],
        heading='Dates'),
        FieldPanel('artists', widget=forms.CheckboxSelectMultiple),
        ImageChooserPanel('featured_image'),
        FieldPanel('featured_image_caption'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

    parent_page_types = ['exhibition.ExhibitionIndexPage']


class ExhibitionPageGalleryImage(Orderable):
    page = ParentalKey(ExhibitionDetailPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
