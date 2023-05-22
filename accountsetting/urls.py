from . import views
from django.urls import path
from .views import CompletePasswordReset


urlpatterns = [
    path('',views.index,name='accountsetting'),
    path('reset-password/', CompletePasswordReset.as_view(),name='reset-password')
]