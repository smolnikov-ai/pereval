from django.urls import path, include
from .views import SubmitData

urlpatterns = [
    path('submitData/', SubmitData.as_view(), name='pass-create'),
    path('submitData/<int:pk>/', SubmitData.as_view(), name='pass-detail'),
]