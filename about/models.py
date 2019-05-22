from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='custom_form_fields')


class FormPage(AbstractEmailForm):
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        InlinePanel('custom_form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email Notification Config"),
    ]

    def get_form_fields(self):
        return self.custom_form_fields.all()


class AboutGalleryPage(Page):

    about_page_title = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    body = RichTextField()
    featured_image = models.ForeignKey(
                    'wagtailimages.Image',
                    null=True,
                    blank=True,
                    on_delete=models.SET_NULL,
                    related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('about_page_title'),
        FieldPanel('body', classname="full"),
        FieldPanel('location'),
        ImageChooserPanel('featured_image'),
    ]


class ContactPage(Page):

    pass
