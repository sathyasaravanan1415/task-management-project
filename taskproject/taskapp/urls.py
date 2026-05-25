from django.urls import path
from . import views
urlpatterns=[
    path('logout/',views.logout_page,name="logout_page"),
    path('login/',views.login_page,name="login_page"),
    path('signup/',views.signup_page,name="signup_page"),
    path('delete/<int:id>/',views.delete_task,name='delete_task'),
    path('update/<int:id>/',views.update_task,name='update_task'),
    path('create/',views.create_task,name='create_task'),
    path('',views.task_list,name='task_list'),
    path('delete_account/',views.delete_account,name="delete_account"),
    path('api/task/<int:task_id>/',views.api_task_list),
    path('api/task/',views.api_task_list),
    path('api/task/update/<int:task_id>/',views.api_update_task),
    path('api/task/delete/<int:task_id>/',views.api_delete_task),
]