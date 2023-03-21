from django.urls import path
from .views import index, SignUpView, CodeConfirmView


board_urlpatterns = [
    path('', index, name='board_index'),
    path('signup', SignUpView.as_view(), name='board_signup'),
    path('signup/<int:pk>/code', CodeConfirmView.as_view(), name='board_code_confirmation'),
]