from django.urls import path
from . import views

urlpatterns = [
    path('',views.JokesFetch.as_view(),name="jokeslist"),
    path('<int:id>',views.JokesDetail.as_view(),name="jokeslist"),
    path('reaction',views.ReactionFetch.as_view(),name="reaction"),
]
