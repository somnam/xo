from django.conf.urls import patterns, url

urlpatterns = patterns(
    # Prefix for all urls in current pattern list
    '',

    url(r'^login/', 'authorization.views.login'),
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login'),
    url(r'^register/', 'authorization.views.register'),
)
