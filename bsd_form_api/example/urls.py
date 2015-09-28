from django.conf.urls import include, url
from example import views

urlpatterns = [
    url(r'^form/', views.example),
]

