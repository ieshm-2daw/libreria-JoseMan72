from django.urls import path
from .views import LibroListView, LibroDetailView, LibroUpdateView, LibroDeleteView, LibroCreateView, LibroLoanView, PrestamosListView, MisLibroListView

urlpatterns = [
    path('',LibroListView.as_view(), name='libro_list'),
    path('detail/<int:pk>/', LibroDetailView.as_view(), name='libro_detail'),
    path('edit/<int:pk>/', LibroUpdateView.as_view(), name='libro_edit'),
    path('delete/<int:pk>/', LibroDeleteView.as_view(), name='libro_delete'),
    path('create/', LibroCreateView.as_view(), name='libro_create'),
    path('loan/<int:pk>/', LibroLoanView.as_view(), name='libro_loan'),
    path('loans/', PrestamosListView.as_view(), name='prestamo_list'),
    path('mislibros/', MisLibroListView.as_view(), name='mislibros_list'),
]