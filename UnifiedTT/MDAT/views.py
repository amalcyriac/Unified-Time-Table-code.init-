from django.shortcuts import render
from django.http import HttpResponse

import csv,io
from django.shortcuts import redirect
from MDAT.models import time_table,students,teachers,courses,slot_time_table
from . import forms
from django.contrib.auth import logout
import ast
# Create your views here.

admin_mails = ["arunjojo999@gmail.com", ]

def home(request):
    logout(request)
    return render(request,'loginpage.html')

def index(request):
    logout(request)
    return HttpResponse("Hello, world !")

def new_admin(request):
    #if not request.user.is_authenticated:
    #        return HttpResponse("Please login as admin")
    #if not request.session.get('id'):
    #   return HttpResponse("This is a page for admin only")
    #sessionID=str(request.session['id'])
    #if sessionID != 'admin':
    #    return HttpResponse("This is a page for admin only")
    #request.session.set_expiry(14400)

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
    return redirect('/fill_time_table_using_dss_data/')
    return HttpResponse("Successfully uploaded, Thank you.")

def update_database_dss(request):
    return HttpResponse("File received thank you!")

def loginsuccess(request):
    if not request.user.is_authenticated:
        return HttpResponse("Google error")

    mail=str(request.user.email)

    if mail in admin_mails:
        request.session['id']='admin'
        request.session.set_expiry(14400)
        output = "Welcome admin<br>Your email is " + mail + "<br>Your session has been created<br>"
        output += "<br>Please goto http://127.0.0.1:8000/student/<br>OR<br>http://127.0.0.1:8000/new_admin/"
        return HttpResponse(output)
        return redirect('/new_admin/')

    if mail[-10:] == "nitc.ac.in":
        request.session['id'] = mail[-20:-11]
        request.session.set_expiry(1200)
        output = "Welcome student<br>Your email is " + mail
        output += "<br>Your Roll No is " + mail[-20:-11] + "<br>Your session has been created<br>"
        output += "<br>Please goto http://127.0.0.1:8000/student/<br>OR<br>http://127.0.0.1:8000/new_admin/"
        return HttpResponse(output)
        return redirect('/student/')
    else:
        request.session['id'] = mail
        request.session.set_expiry(1200)
        output = "Welcome teacher<br>Your email is " + mail + "<br>Your session has been created<br>"
        output += "<br>Please goto http://127.0.0.1:8000/student/<br>OR<br>http://127.0.0.1:8000/new_admin/"
        return HttpResponse(output)
        return redirect('/teacher/')

def fill_time_table_using_dss_data(request):
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

    return HttpResponse("Database updated, you can go to http://127.0.0.1:8000/")





def find_tt_both(id, type):
    if type == 'student':
        studentORteacherData = students.objects.values().filter(student_id = id.lower())
    else:
        studentORteacherData = teachers.objects.values().filter(teacher_id = id.lower())

    coursesAndBatches = []

    for row in studentORteacherData:
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

    return ans

def find_tt_student(request):
    template = "home_student.html"
    if request.method == "GET":
        form = forms.roll_no()
        return render(request,template,{'form':form})

    form = forms.roll_no(request.POST)
    if form.is_valid():
        input_roll_no = form.cleaned_data['roll_no'].lower()

        studentsWithThisRoll = students.objects.values().filter(student_id=input_roll_no)
        teachersWithThisId = teachers.objects.values().filter(teacher_id=input_roll_no)
        ans = None
        if len(studentsWithThisRoll) > 0:
            ans = find_tt_both(input_roll_no, 'student')
            request.session['type'] = "student"
            request.session['id'] = input_roll_no
        elif len(teachersWithThisId) > 0:
            ans = find_tt_both(input_roll_no, 'teacher')
            request.session['type'] = "teacher"
            request.session['id'] = input_roll_no
        else:
            return HttpResponse("Error, give valid input for roll no")

        return render(request,'home_student.html',{'form':form,'var3':ans,})

def find_free_slots(request):
    if request.session['type'] != "teacher":
        return HttpResponse("Only teacher can change timetable")
    teacherID = request.session['id']

    fromDay = request.POST.get('fname',None)
    fromHour = request.POST.get('st',None)

    teacherTT = find_tt_both(teacherID, "teacher")
    freeSlotsOfTeacher = []
    for teacherTTDay in teacherTT:
        for i in range(1,10):
            if teacherTTDay['hour'+str(i)] == "":
                freeSlotsOfTeacher.append((teacherTTDay["dayNum"],str(i)))

    teacherRows = teachers.objects.values().filter(teacher_id=teacherID)
#listset
    batchesThisTeacherTeach = []
    for row in teacherRows:
        batchesThisTeacherTeach.append(row['batch_id'])
    studentsInTheseBatches = []
    allStudents = students.objects.values()
    for studentRow in allStudents:
        if studentRow['batch_id'] in batchesThisTeacherTeach:
            studentsInTheseBatches.append(studentRow['student_id'])
    studentsInTheseBatches = list(set(studentsInTheseBatches))

    batchesTheseStudentsStudy = []
    for stud in studentsInTheseBatches:
        studData = allStudents.filter(student_id=stud)
        for row in studData:
            batchesTheseStudentsStudy.append(row['batch_id'])
    batchesTheseStudentsStudy = list(set(batchesTheseStudentsStudy))

    possibleFreeSlots = []
    curTT = time_table.objects.values()
    for freeSlotOfTeacher in freeSlotsOfTeacher:
        freeDay = freeSlotOfTeacher[0]
        freeHour = freeSlotOfTeacher[1]
        include = True
        for batch in batchesTheseStudentsStudy:
            schedule = curTT.filter(batch_id=batch)[0]['allocation']
            schedule = ast.literal_eval(schedule)
            if schedule[int(freeDay)-1][int(freeHour)-1] != "0":
                include = False
                if freeDay == "2" and freeHour == "1":
                    return HttpResponse("hi")
        if include == True:
            possibleFreeSlots.append(freeSlotOfTeacher)

    for day,hour in possibleFreeSlots:
        day = int(day)-1
        hour = 'hour' + hour
        teacherTT[day][hour] = "Free"

    return render(request,'home_student.html',{'var3':teacherTT})
