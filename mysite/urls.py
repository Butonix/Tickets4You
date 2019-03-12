from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views import defaults as default_views

from core.views import index, offers, contact, companies, feedback, hotels, blog, single_blog, schedules, book_now, cancel_now

urlpatterns = [
    re_path(r'^$', index, name="index"),
    re_path(r'^offers/$', offers, name="offers"),
    re_path(r'^contact/$', contact, name="contact"),
    re_path(r'^companies/$', companies, name="companies"),
    re_path(r'^feedback/$', feedback, name="feedback"),
    re_path(r'^hotels/$', hotels, name="hotels"),
    re_path(r'^blog/$', blog, name="blog"),
    re_path(r'^blog/(?P<slug>[-\w]+)/$', single_blog, name="single_blog"),
    re_path(r'^schedules/$', schedules, name="schedules"),
    re_path(r'^book_now/$', book_now, name="book_now"),
    re_path(r'^cancel_now/$', cancel_now, name="cancel_now"),
    # users urls
    re_path(r'^profile/', include('users.urls')),
    # allauth urls
    re_path(r'^accounts/', include('allauth.urls')),
    # django auth urls
    re_path(r'^', include('django.contrib.auth.urls')),
    # admin urls
    path('admin/', admin.site.urls),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
) + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development
    urlpatterns += [
        re_path(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        re_path(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        re_path(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        re_path(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            re_path(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
