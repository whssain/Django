from django.conf.urls import url
from .views import PostListAPIView ,PostDetailAPIView,PostDeleteAPIView,PostCreateAPIView


urlpatterns = [
    url(r'^list/$', PostListAPIView.as_view(), name="list"),
    url(r'^create/$', PostCreateAPIView.as_view(), name="create"),
    url(r'^detail/(?P<post_slug>[-\w]+)/$', PostDetailAPIView.as_view(), name="detail"),
    url(r'^delete/(?P<post_slug>[-\w]+)/$', PostDeleteAPIView.as_view(), name="delete"),
    
]