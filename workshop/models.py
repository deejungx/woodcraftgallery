from django import forms
from django.db import models
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index

@register_snippet
class Medium(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=100)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Medium"
        verbose_name_plural = "Mediums"

class WorkshopIndexPage(Page):

    def get_context(self, request):
        context = super().get_context(request)
        context['workshops'] = WorkshopDetailPage.objects.live().child_of(self).all()
        return context


class WorkshopDetailPage(Page):

    workshop_title = models.CharField(max_length=250)
    medium = ParentalManyToManyField('workshop.Medium', blank=True)
    medium_detail = models.CharField(max_length=250, blank=True, null=True)
    introduction = RichTextField()
    duration = models.IntegerField()
    price = models.CharField(max_length=250, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    extra_information = models.CharField(max_length=250, blank=True, null=True)

    def main_image(self):
        gallery_item = self.workshop_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('workshop_title'),
        FieldPanel('medium', widget=forms.CheckboxSelectMultiple),
        FieldPanel('medium_detail'),
        FieldPanel('introduction', classname="full"),
        FieldPanel('duration'),
        FieldPanel('price'),
        FieldPanel('date'),
        FieldPanel('time'),
        FieldPanel('extra_information'),
        InlinePanel('workshop_images', label="Workshop images"),
    ]

    parent_page_types = ['workshop.WorkshopIndexPage']


class WorkshopGalleryImage(Orderable):
    page = ParentalKey(WorkshopDetailPage, on_delete=models.CASCADE, related_name='workshop_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
