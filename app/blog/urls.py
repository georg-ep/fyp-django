from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/create', views.PostCreateView.as_view({'post': 'create'}), name='post_create'),
    path('posts/update/<int:pk>', views.PostUpdateDestroyView.as_view({'patch': 'patch'}), name='post_update'),
    path('posts/delete/<int:pk>', views.PostUpdateDestroyView.as_view({'delete': 'destroy'}), name='post_destroy'),
    path('posts/detail/<slug>', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/retreive/<int:pk>', views.PostOwnerDetail.as_view(), name='post_owner_detail'),
    path('posts/image/add/', views.ImageCreateView.as_view(), name='post_image_add'),
    path('posts/image/delete/<int:pk>', views.ImageDeleteUpdateView.as_view({"delete": "destroy"}), name='image_delete'),
    path('posts/image/update/<int:pk>', views.ImageDeleteUpdateView.as_view({"patch": "patch"}), name='image_update'),
    path('posts/comment/create', views.PostCommentCreateView.as_view(), name='create_comment'),
    path('posts/comments/<slug>', views.PostCommentListView.as_view(), name='list_comment'),
    path('posts/comments/delete/<int:pk>', views.PostCommentDeleteView.as_view(), name='delete_comment'),

]
