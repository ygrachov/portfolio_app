from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'app'
urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('<int:pk>/favorite/', AddFavorite.as_view(), name='forum_favorite'),
    path('<int:pk>/unfavorite/', DeleteFavorite.as_view(), name='forum_unfavorite'),
    path('create_forum/', CreateForum.as_view(), name='create_forum'),
    path('<int:pk>/forum_details', ForumDetailsView.as_view(), name='forum_details'),
    path('<int:pk>', UpdateForum.as_view(), name='update_forum'),
    path('<int:pk>/delete_forum', DeleteForum.as_view(), name='delete_forum'),
    path('pic_picture/<int:pk>', stream_file, name='pic_picture'),
    path('comment/<int:pk>/comment/', CommentCreateView.as_view(), name='forum_comment_create'),
    path('comment/<int:pk>/comments_form', CommentUpdateView.as_view(), name="forum_comment_edit"),
    path('comment/<int:pk>/delete_comment', CommentDeleteView.as_view(), name='delete_comment')
]

social_login = 'registration/login.html'
urlpatterns.insert(0,
                   path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'))
                   )
