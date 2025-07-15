from django.urls import path, include
from .views import SubmitData

urlpatterns = [
    path('create/', SubmitData.as_view(), name='pass-create'),
]