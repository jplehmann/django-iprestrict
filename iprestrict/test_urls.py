# This file is to be used for testing only

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('iprestrict.views',
    url(r'^iprestrict/move_rule_up/(?P<rule_id>\d+)[/]?$', 'move_rule_up'),
    url(r'^iprestrict/move_rule_down/(?P<rule_id>\d+)[/]?$', 'move_rule_down'),
    url(r'^iprestrict/reload_rules[/]?$', 'reload_rules'),
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

