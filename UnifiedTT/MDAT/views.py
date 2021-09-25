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
            var1 = students.objects.values().filter(student_id = input_roll_no.lower())

            #for item in var1:
            #    print(item)
            #print(var1)

            var2 = []
            for item in var1:
                temp = item['course_id']
                var2.extend(courses.objects.values().filter(course_id = temp))
            #print(var2)

            var3 = []
            slots = []
            slot_subject_map = {}
            for item in var2:
                temp = item['slot']
                slots.extend(temp)
                slot_subject_map[item['slot']] = item['course_name']
            var3 = slot_time_table.objects.values().all()
            #print(var3)

            for item in var3:
                if item["hour1"] not in slots:
                    item["hour1"] = ""
                if item["hour2"] not in slots:
                    item["hour2"] = ""
                if item["hour3"] not in slots:
                    item["hour3"] = ""
                if item["hour4"] not in slots:
                    item["hour4"] = ""
                if item["hour5"] not in slots:
                    item["hour5"] = ""
                if item["hour6"] not in slots:
                    item["hour6"] = ""
                if item["hour7"] not in slots:
                    item["hour7"] = ""
                if item["hour8"] not in slots:
                    item["hour8"] = ""
                if item["hour9"] not in slots:
                    item["hour9"] = ""
            for item in var3:
                if item["hour1"] in slots:
                    item["hour1"] = slot_subject_map[item["hour1"]]
                if item["hour2"] in slots:
                    item["hour2"] = slot_subject_map[item["hour2"]]
                if item["hour3"] in slots:
                    item["hour3"] = slot_subject_map[item["hour3"]]
                if item["hour4"] in slots:
                    item["hour4"] = slot_subject_map[item["hour4"]]
                if item["hour5"] in slots:
                    item["hour5"] = slot_subject_map[item["hour5"]]
                if item["hour6"] in slots:
                    item["hour6"] = slot_subject_map[item["hour6"]]
                if item["hour7"] in slots:
                    item["hour7"] = slot_subject_map[item["hour7"]]
                if item["hour8"] in slots:
                    item["hour8"] = slot_subject_map[item["hour8"]]
                if item["hour9"] in slots:
                    item["hour9"] = slot_subject_map[item["hour9"]]
            print(var3)
            for item in var3:
                if item["day"] == '1':
                    item["day"] = "Monday"
                elif item["day"] == '2':
                    item["day"] = "Tuesday"
                elif item["day"] == '3':
                    item["day"] = "Wednesday"
                elif item["day"] == '4':
                    item["day"] = "Thursday"
                elif item["day"] == '5':
                    item["day"] = "Friday"

            return render(request,'home_student.html',{'form':form,'var3':var3,})

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
