from django.urls import path
from . import views

urlpatterns = [
    path('build/ga', views.build_with_ga, name='build_with_ga'),
    path('build/ts', views.build_with_ts, name='build_with_ts'),
]
