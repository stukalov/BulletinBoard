from django.urls import path
from .views import *


board_urlpatterns = [
    path('signup', SignUpView.as_view(), name='board_signup'),
    path('signup/<int:pk>/code', CodeConfirmView.as_view(), name='board_code_confirmation'),
    path('', BulletinList.as_view(), name='bulletin_list'),
    path('my', BulletinMyList.as_view(), name='bulletin_my_list'),
    path('bulletin', BulletinCreate.as_view(), name='bulletin_create'),
    path('bulletin/<int:pk>', BulletinDetail.as_view(), name='bulletin_detail'),
    path('bulletin/<int:pk>/edit', BulletinUpdate.as_view(), name='bulletin_edit'),
    path('bulletin/<int:pk>/delete', BulletinDelete.as_view(), name='bulletin_delete'),
    path('bulletin/<int:bulletin>/replay', ReplayCreate.as_view(), name='bulletin_replay'),
    path('my_replay/<int:pk>', ReplayMyDetail.as_view(), name='replay_my_detail'),
    path('my_replays', ReplayMyList.as_view(), name='replay_my_list'),
    path('replay/<int:pk>', ReplayDetail.as_view(), name='replay_detail'),
    path('replays', ReplayList.as_view(), name='replay_list'),
    path('replay/<int:pk>/accept', ReplayAccept.as_view(), name='replay_accept'),
    path('replay/<int:pk>/decline', ReplayDecline.as_view(), name='replay_decline'),
]