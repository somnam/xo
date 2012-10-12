from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',

    # Examples:
    # url(r'^$', 'xo.views.home', name='home'),
    # url(r'^xo/', include('xo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'go.views.read', name='home'),
    
    # Auth views
    url(r'^', include('auth.urls')),

    # Go views
    url(r'^go/', include('go.urls')),
)
