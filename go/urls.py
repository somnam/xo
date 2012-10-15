from django.conf.urls import patterns, url

urlpatterns = patterns(
    'go.views',

    # Get list of games
    url(r'^$', 'game_list'),

    ## Create new game
    #url(r'^create/', 'game_create'),

    ## Join game
    #url(r'^(?P<game_id>\d+)/join/$', 'join'),

    ## Update game
    #url(r'^(?P<game_id>\d+)/update/$', 'update'),

    ## Delete game
    #url(r'^(?P<game_id>\d+)/delete/$', 'delete'),

    # Test game board
    url(r'^test/', 'test'),
)

