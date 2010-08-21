from django.conf.urls.defaults import patterns, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^events/femtec-2011/', include('femtec.site.views')),
    (r'^events/femtec-2011/admin/(.*)', admin.site.root),
)

handler404 = 'femtec.site.views.handler404'
handler500 = 'femtec.site.views.handler500'

