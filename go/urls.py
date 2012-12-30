from django.conf.urls import patterns, url

urlpatterns = patterns(
    'go.views',

    # Get list of games
    url(r'^$', 'game_list'),

    # Create new game
    url(r'^create/', 'game_create'),

    # Join game
    url(r'^(?P<game_id>\d+)/join/$', 'game_join'),

    # Play game
    url(r'^(?P<game_id>\d+)/play/$', 'game_play'),

    # Edit game settings
    url(r'^(?P<game_id>\d+)/edit/$', 'game_edit'),

    # Update game state
    url(r'^(?P<game_id>\d+)/update/$', 'game_update'),

    # Delete game
    url(r'^(?P<game_id>\d+)/delete/$', 'game_delete'),
)

