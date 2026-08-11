from django.urls import path
from . import views

urlpatterns = [
    path(route='', view=views.index, name='index'),
    path(route='about/', view=views.about, name='about'),
    path(route='gallery/', view=views.gallery, name='gallery'),
    path(route='contact', view=views.contact, name='contact'),
]