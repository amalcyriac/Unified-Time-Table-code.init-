from django.contrib import admin

# Register your models here.

from MDAT.models import time_table,students,teachers,courses,slot_time_table
admin.site.register(time_table)
admin.site.register(students)
admin.site.register(teachers)
admin.site.register(courses)
admin.site.register(slot_time_table)
