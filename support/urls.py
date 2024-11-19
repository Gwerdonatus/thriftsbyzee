from django.urls import path
from .views import interactive_page, delete_review

urlpatterns = [
    path('interactive-page/', interactive_page, name='interactive_page'),
    path('delete-review/<int:id>/', delete_review, name='delete_review'),
]
