from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
import csv,io
from MDAT.models import time_table,students,teachers,courses,slot_time_table
from . import forms
#from django.contrib.auth import logout

def index(request):
    return HttpResponse("Hello, world !")

def new_admin(request):
    template="admin_page.html"
    if request.method == "GET":
        return render(request,template)

    csv_file_1 = request.FILES['students_file']
    if not csv_file_1.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')
    students.objects.all().delete()
    data_set = csv_file_1.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = students.objects.update_or_create(
            student_id=column[0].lower(),
            course_id=column[1],
            batch_id=column[2]
        )

    csv_file_2 = request.FILES['teachers_file']
    if not csv_file_2.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')
    teachers.objects.all().delete()
    data_set = csv_file_2.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = teachers.objects.update_or_create(
            teacher_id=column[0].lower(),
            course_id=column[1],
            batch_id = column[2]
        )
    csv_file_3 = request.FILES['courses_file']
    if not csv_file_3.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')
    courses.objects.all().delete()
    data_set = csv_file_3.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = courses.objects.update_or_create(
            course_id = column[0],
            course_name = column[1],
            slot = column[2]
        )

    csv_file_4 = request.FILES['slots_file']
    if not csv_file_4.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')
    slot_time_table.objects.all().delete()
    data_set = csv_file_4.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = slot_time_table.objects.update_or_create(
            day = column[0],
            hour1 = column[1],
            hour2 = column[2],
            hour3 = column[3],
            hour4 = column[4],
            hour5 = column[5],
            hour6 = column[6],
            hour7 = column[7],
            hour8 = column[8],
            hour9 = column[9]
        )

    return HttpResponse("Successfully uploaded, Thank you.")

def update_database_dss(request):
    return HttpResponse("File received thank you!")
