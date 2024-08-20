from django.urls import path
from .views import TaxonomyViewSet

urlpatterns = [
    path('taxonomy/all/', TaxonomyViewSet.as_view({'get': 'list'}), name='taxonomy-list-create'),

    path('taxonomy/create/', TaxonomyViewSet.as_view({'post': 'create'}), name='taxonomy-create'),

    path('taxonomy/<int:pk>/', TaxonomyViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='taxonomy-detail'),
]
