from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import SnippetViewSet, UserViewSet
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from pdb import set_trace


app_name = 'snippets'

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

# snippet_list = SnippetViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })

# snippet_detail = SnippetViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })

# snippet_highlight = SnippetViewSet.as_view({
#     'get': 'highlight'
# }, renderer_classes=[renderers.StaticHTMLRenderer])

# user_list = UserViewSet.as_view({
#     'get': 'list'
# })

# user_detail = UserViewSet.as_view({
#     'get': 'retrieve'
# })


# urlpatterns = [
#     path('', api_root),
#     path('snippets/', snippet_list, name='snippet-list'),
#     path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
#     path('snippets/highlight/<int:pk>/', snippet_highlight, name='snippet-highlight'),
#     path('users/', user_list, name='users-list'),
#     path('users/detail/<int:pk>/', user_detail, name='users-detail')
# ]

# urlpatterns = [
#     path('', views.api_root),
#     path('snippets/', views.ConcisedGenericSnippetList.as_view(), name='snippet-list'),
#     path('snippets/<int:pk>/', views.ConcisedGenericSnippetDetail.as_view(), name='snippet-detail'),
#     path('snippets/<int:pk>/heighlighted', views.GenericSnippetHeighlight.as_view(), name='snippet-highlight'),
#     path('users/', views.ConcisedGenericUserList.as_view(), name='users-list'),
#     path('users/<int:pk>/', views.ConcisedGenericUserDetail.as_view(), name='users-detail'),
# ]

# urlpatterns = format_suffix_patterns(urlpatterns)