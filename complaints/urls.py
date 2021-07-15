from . import views
from django.urls import path, include

urlpatterns = [
    path('create',views.create,name = 'create'),
    path('detail',views.for_user, name = 'detail'),
    path('admin_detail',views.for_admin, name = 'detail_admin'),
    path('mail_sent',views.mail_sent,name ='mail_sent'),
    path('analytics_system',views.analytics_system,name ='analytics_system'),
    path('costs',views.costs,name= 'costs'),
    path('admin_costs',views.admin_costs, name='admin_costs'),
    path('history',views.history, name = 'history'),
    path('<int:complaint_id>',views.specific , name = 'specific'),
    path('<int:complaint_id>/approve',views.approve,name = 'approve'),
    path('<int:complaint_id>/pending',views.pending,name = 'pending'),
    path('<int:complaint_id>/rejected',views.rejected,name = 'rejected'),
    path('<int:complaint_id>/delete',views.delete,name = 'delete'),
    path('<int:complaint_id>/rate',views.rate,name = 'rate'),
    path('<int:complaint_id>/email_personel',views.email_personel,name = 'email_personel')
]
