"""chicago URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin

from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from manager.sites import site

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^chaining/', include('smart_selects.urls')),

    url(r'^articles/', include('articles.urls')),
    url(r'^advertisement/', include('advertisement.urls')),
    url(r'^podcast/', include('podcast.urls')),
    url(r'^manager/', include(site.urls)),

    url(r'^auth/', include('authenticate.urls')),
    url(r'^', include('app.urls')),
    

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#urlpatterns += i18n_patterns(
#        url(_(r'^auth/'), include('authenticate.urls')),
#        url(_(r'^'), include('app.urls')),
#    )

urlpatterns += [
    url(r'^media/(?P<path>.*)$', serve, { 'document_root': settings.MEDIA_ROOT, }),
    url(r'^static/(?P<path>.*)$', serve, { 'document_root': settings.STATIC_ROOT }),
    ]
