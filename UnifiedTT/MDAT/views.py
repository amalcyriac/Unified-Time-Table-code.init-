from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
import csv,io
from MDAT.models import time_table,students,teachers,courses,slot_time_table
from . import forms
#from django.contrib.auth import logout
from django.core import serializers
from django.http import JsonResponse

import ast
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
    time_table.objects.all().delete()
    return HttpResponse("Successfully uploaded, Thank you.")

def find_tt_student(request):

    template = "home_student.html"
    if request.method == "GET":
        form = forms.roll_no()
        return render(request,template,{'form':form})

    form = forms.roll_no(request.POST)
    if form.is_valid():
        input_roll_no = form.cleaned_data['roll_no']
        if students.objects.filter(student_id__icontains = input_roll_no).exists() :
            studentData = students.objects.values().filter(student_id = input_roll_no.lower())

            coursesAndBatches = []

            for row in studentData:
                coursesAndBatches.append((row['course_id'], row['batch_id']))

            ttRows = time_table.objects.values()
            ans = [{},{},{},{},{}]
            for i in range(5):
                for j in range(1,10):
                    ans[i]['hour'+str(j)] = ""
            for course, batch in coursesAndBatches:
                courseName = courses.objects.values().filter(course_id=course)[0]['course_name']
                ttRow = ttRows.filter(course_id=course,batch_id=batch)[0]
                scheduleForSubject = ttRow['allocation']
                scheduleForSubject = ast.literal_eval(scheduleForSubject)

                for dayIndex in range(5):
                    day = str(dayIndex+1)
                    ans[dayIndex]['dayNum'] = day
                    if day == "1":
                        ans[dayIndex]['day'] = "Monday"
                    elif day == "2":
                        ans[dayIndex]['day'] = "Tuesday"
                    elif day == "3":
                        ans[dayIndex]['day'] = "Wednesday"
                    elif day == "4":
                        ans[dayIndex]['day'] = "Thursday"
                    elif day == "5":
                        ans[dayIndex]['day'] = "Friday"

                    scheduleForSubjectDay = scheduleForSubject[dayIndex]
                    for hour in range(9):
                        if scheduleForSubjectDay[hour] == "1":
                            ans[dayIndex]['hour'+str(hour+1)] = courseName
                            ans[dayIndex]['hour'+str(hour+1)+"coursecode"] = course
                            ans[dayIndex]['hour'+str(hour+1)+"batch"] = batch
            return render(request,'home_student.html',{'form':form,'var3':ans,})

        else :
            return HttpResponse("Error")


def fill_time_table_using_dss_data(request):
    # _,row=credited_courses_table.objects.update_or_create(roll_no=roll,faculty_name='SUSHANT VARMA',course_name='MATHEMATICS',feedback_status=0)
    time_table.objects.all().delete()
    courses_rows=courses.objects.values()
    for courses_row in courses_rows:
        course_id = courses_row['course_id']
        slot = courses_row['slot']
        students_with_this_course = students.objects.values().filter(course_id=course_id)
        batches_with_this_course = []
        for students_row in students_with_this_course:
            batch_id = students_row['batch_id']
            if not batch_id in batches_with_this_course:
                batches_with_this_course.append(batch_id)
        schedule = []
        global_time_table = slot_time_table.objects.values()
        for dayIndex in range(5):
            schedule_of_day = ["0", "0", "0", "0", "0", "0", "0", "0", "0"]
            global_schedule_of_day = global_time_table[dayIndex]
            for hourIndex in range(1,10):
                if global_schedule_of_day['hour'+str(hourIndex)] == slot:
                    schedule_of_day[hourIndex-1] = "1";

            schedule.append(schedule_of_day.copy())

        for batch in batches_with_this_course:
             _,row=time_table.objects.update_or_create(course_id=course_id,batch_id=batch,allocation=schedule)

    return HttpResponse("Thanks")
