from django.conf.urls import *

urlpatterns = patterns("",
    # One url. How embarrassing.
    url(r'^import/$', 'scraper.views.importer'),
)
