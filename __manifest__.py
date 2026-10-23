# -*- coding: utf-8 -*-
# Part of Odoo.

{
    'name' : 'Hotel Management invoicing',
    'depends' : ['account'],
    'version' : '18.0.1.0',
    'summary' : '',
    'sequence' :'1',
    'description' : 'It is a demo hotel management system module',
    
    "data": [
        "security/ir.model.access.csv",
        "wizards/show_rooms.xml",
        "data/room_booking_sequence.xml",
        "data/email_template.xml",
        "views/booking_order_lines.xml",
        "views/Food.xml",
        "views/hotel_amenities_view.xml",
        "views/hotel_guest_view.xml",
        "views/hotel_policies_view.xml",
        "views/hotel_room_kanban.xml",
        "views/hotel_room_view.xml",
        "views/hotel_service_view.xml",
        "views/hotel_user_view.xml",
        "views/hotel_view.xml",
        "views/housekeeping_report.xml",
        "views/HouseKeepingMaintenanceService.xml",
        "views/HouseKeepingMaintenancetype.xml",
        "views/HousekeepingPlanning.xml",
        "views/HouseKeepingStaff.xml",
        "views/HousekeepingStaffEntry.xml",
        "views/maintenance_checklist_service_views.xml",
        "views/Restaurant.xml",
        "views/room_booking_view.xml",
        "views/room_price_view.xml",
        "views/room_specification.xml",
        "views/room_type_view.xml",
        "views/season_view.xml",
        "views/menus.xml",
    ],

    'installable': True,
    'application': True,
    'auto_install': True,
    'license': 'LGPL-3'
}