from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'snippets'

urlpatterns = [
    path('snippets/', views.view_list_snippets),
    path('snippets/<int:pk>/', views.view_snippet_detail)
]

urlpatterns = format_suffix_patterns(urlpatterns)