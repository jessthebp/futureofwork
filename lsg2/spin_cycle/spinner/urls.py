from django.urls import path

from . import views

urlpatterns = [
  path("", views.ProjectList.as_view(), name='home'),
  path("project/list", views.ProjectList.as_view(), name="projectlist"),
  path("project/create", views.ProjectCreate.as_view(), name="projectcreate"),
  path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail_view'),
  path('project/<int:pk>/update/', views.ProjectUpdate.as_view(), name='project_update_view'),
  path('project/<int:pk>/delete/', views.ProjectDelete.as_view(), name='project_delete_view'),
    path('project/<int:pk>/pieceinputs/', views.piece_inputs, name='piece_inputs'),
    path('project/<int:pk>/piecebackgrounds/', views.piece_backgrounds, name='piece_backgrounds'),
path('project/<int:project_id>/pieces/', views.piece_inputs_for_project, name='piece_inputs_for_project'),
  path('projects/', views.ProjectList.as_view(), name='project_list'),
]