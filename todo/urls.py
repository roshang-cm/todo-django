from django.urls import path
import todo.views as views

app_name = 'todo'
urlpatterns = [
    path('', views.index, name='index_view'),
    path('add', views.add_todo, name='add_view'),
    path('<int:todo_id>/status', views.change_status),
    path('<int:todo_id>/delete', views.delete_todo),
    path('login', views.login, name='login_view'),
    path('signup', views.signup, name='signup_view')
]
