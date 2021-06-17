from django.urls import path

from . import views

urlpatterns = [
    path('v1/journal', views.journal_records),
    path('v1/last', views.last_record),
    path('v1/cars', views.car_list),
    path('v1/cameras', views.get_all_cameras),
    path('v1/options', views.option_get),
    path('v1/add', views.add_all),
    path('v1/delete', views.delete_all),
    path('v1/update', views.upd_all),
    path('v1/feedback', views.feedback),
    path('v1/open', views.open_barrier),
    path('v1/test', views.test),
    path('v1/addrec', views.create_records),
    path('v1/barrier/allrec', views.view_all),
    path('v1/filters', views.multiple_filters),
    path('v1/set_timer', views.set_timer),
    path('v1/get_timer', views.get_timer)
]
