"""Copyright Askbot SpA 2014, Licensed under GPLv3 license."""

from django.urls import path


from directory import views

urlpatterns = (
    path(r'<path:path>', views.browse, name='directory_browse'),
)
