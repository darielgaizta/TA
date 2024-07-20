from django.urls import path
from . import views

urlpatterns = [
    path('build/ga', views.build_with_ga, name='build_with_ga'),
    path('build/ts', views.build_with_ts, name='build_with_ts'),
    path('preset/ga', views.preset_with_ga, name='preset_with_ga'),
    path('preset/ts', views.preset_with_ts, name='preset_with_ts'),

    path('ui/build', views.ui_build, name='ui_build')
]
