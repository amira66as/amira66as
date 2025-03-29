from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # ✅ فقط این کافیه
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),  # این مسیر پیش‌فرض است و به صفحه اصلی هدایت می‌شود
    path('register/company/', views.register_company, name='register_company'),
    path('register/employee/', views.register_employee, name='register_employee'),
    path('dashboard/', views.company_dashboard, name='company_dashboard'),
    path('login/', views.login_view, name='login'),
    path("logout/", views.logout_user, name="logout"),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('my_employee/', views.myemployee, name='my_employee'),
    path('my_colleagues/', views.mycolleagues, name='my_colleagues'),
    path('nezarat/', views.nezarat, name='nezarat'),
    path('nezaratc/', views.nezaratc, name='nezaratc'),
    path('chat/<int:receiver_id>/', views.chat_view, name='chat'),
    path('create-warehouse/', views.create_warehouse, name='create_warehouse'),
    path('add-part-to-warehouse/', views.add_part_to_warehouse, name='add_part_to_warehouse'),
    path('warehouse-list/', views.warehouse_list, name='warehouse_list'),
    path('update-warehouse/<int:warehouse_id>/', views.update_warehouse, name='update_warehouse'),
    path('delete-warehouse/<int:warehouse_id>/', views.delete_warehouse, name='delete_warehouse'),
    path('update-ship/<int:ship_id>/', views.update_ship, name='update_ship'),
    path('delete-ship/<int:ship_id>/', views.delete_ship, name='delete_ship'),
    path('export/searched-ship/', views.export_searched_ship_to_excel, name='export_searched_ship_to_excel'),
    path('reminders/', views.reminder_list, name='reminder_list'),
    path('reminders/create/', views.create_reminder, name='create_reminder'),
    path('reminders/update/<int:reminder_id>/', views.update_reminder, name='update_reminder'),
    path('reminders/delete/<int:reminder_id>/', views.delete_reminder, name='delete_reminder'),
    path('subwarehouse/edit/<int:subwarehouse_id>/', views.update_subwarehouse, name='update_subwarehouse'),
    path('part/wornout/<int:part_id>/', views.mark_worn_out, name='mark_worn_out'),
    path('transport/create/', views.create_transport_operation, name='create_transport_operation'),
    path('transport/<int:operation_id>/add-items/', views.add_transport_items, name='add_transport_items'),
    path('transport/list/', views.transport_list, name='transport_list'),
    path('transport/<int:operation_id>/detail/', views.transport_detail, name='transport_detail'),
    path('transport/<int:operation_id>/add-multi-items/', views.add_multiple_transport_items, name='add_multiple_transport_items'),
    path('transport/<int:operation_id>/export-pdf/', views.export_transport_pdf, name='export_transport_pdf'),
    path('warehouse/add-substorage/', views.create_warehouse_substorage, name='create_warehouse_substorage'),
    path('ship/add-attribute/', views.add_ship_attribute, name='add_ship_attribute'),
    path('report-damage/', views.report_damage, name='report_damage'),
    path('review-damage/', views.review_damage_reports, name='review_damage_reports'),
    path('confirm-damage/<int:report_id>/', views.confirm_damage_report, name='confirm_damage_report'),
    path('parts/status-report/', views.part_status_report, name='part_status_report'),
    path('dashboard/role/', views.role_based_dashboard, name='role_based_dashboard'),
    path('damage-reports/', views.review_damage_reports, name='review_damage_reports'),
    path('damage-reports/<int:report_id>/<str:action>/', views.handle_damage_report, name='handle_damage_report'),
    path('transport/<int:operation_id>/export/excel/', views.export_transport_excel, name='export_transport_excel'),
    path('ship/<int:ship_id>/visual/', views.ship_visual_dashboard, name='ship_visual_dashboard'),
    path('create_warehouse/', views.create_warehouse, name='create_warehouse'),
    path('create_warehouse_substorage/', views.create_warehouse_substorage, name='create_warehouse_substorage'),
    path('create_ship/', views.create_ship, name='create_ship'),
    path('create_ship_subwarehouse/', views.create_ship_subwarehouse, name='create_ship_subwarehouse'),
    path('create_transport_operation/', views.create_transport_operation, name='create_transport_operation'),
    path('create_part/', views.create_part, name='create_part'),
    path('transport_operation_list/', views.transport_operation_list, name='transport_operation_list'),
    path('part_list/', views.part_list, name='part_list'),
    path('chat/', views.chat_list, name='chat_list'),
    path('update_part/<int:id>/', views.update_part, name='update_part'),  # تعریف URL
    path('warehouses/', views.warehouse_list, name='warehouse_list'),
    path('warehouses/new/', views.create_warehouse_with_substorages, name='create_warehouse_with_substorages'),
    path('damage-reports/', views.review_damage_reports, name='review_damage_reports'),
    path('warehouse-details/<int:warehouse_id>/', views.warehouse_details, name='warehouse_details'),
    path('ship-details/<int:ship_id>/', views.ship_details, name='ship_details'),
    path('ships/delete-ajax/<int:ship_id>/', views.delete_ship_ajax, name='delete_ship_ajax'),
    path('ships/edit-modal/<int:ship_id>/', views.edit_ship_modal, name='edit_ship_modal'),
    path('ships/delete-ajax/<int:ship_id>/', views.delete_ship_ajax, name='delete_ship_ajax'),
    




    

]














