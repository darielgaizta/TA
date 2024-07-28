from django.urls import path
from . import views, api

urlpatterns = [
    path('build/ga', api.build_with_ga, name='build_with_ga'),
    path('build/ts', api.build_with_ts, name='build_with_ts'),
    path('preset/ga', api.preset_with_ga, name='preset_with_ga'),
    path('preset/ts', api.preset_with_ts, name='preset_with_ts'),

    path('ui/build', views.build, name='ui_build'),
    path('ui/preset', views.preset, name='ui_preset')
]
