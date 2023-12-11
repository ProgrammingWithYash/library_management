from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('issued/', views.issued, name='issued'),
    path('add/', views.add, name='add'),
    path('addInsert/', views.addInsert, name='addInsert'),
    path('issue/', views.issue, name='issue'),
    path('issueInsert/', views.issueInsert, name='issueInsert'),
    path('bookdelete/', views.bookdelete, name='bookdelete'),
    path('issuedelete/', views.issuedelete, name='issuedelete'),
    path('editbook/', views.addEdit, name='addEdit'),
    path('editissue/', views.issueEdit, name='issueEdit'),
]
