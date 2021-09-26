# Unified-Time-Table

Unified Time Table Project for Codeinit Hackathon

**Problem**
To change a course timing, students / teachers take a lot of time since they have to check the time table of that teacher and the time table of all students who took that course (including seniors and juniors). Then they have to find a timing that does not clash with any elective. Also, students need to create time table using 3rd party tools customized to their electives since they are only given the slot-time table (like slot A, slot B). Moreover, CR needs to circulate google form to find interest of students concerning a change in timetable


**How to use this**
Once the necessary data is obtained from dss, students/teachers can login and see their time table (with their course names instead of slot names)
An example data (csv) from dss is included in the root
Students/teachers/admin need to login through nitc mail (google-allauth)
admin can add dss data
If needed, teachers can see which slots are free for a subject. The website will check all the free periods of teacher first, then list all the students who study in that batch for that course, then check their timetable(including electives) and then displays the available slots

Note : g-auth will only run on machines configured with the google client key and secret key. In order to make it public (so that we can see/edit timetable without gmail), we have separated the gauth. (gauth working can be shown during presentation)

Install django, postgresql, psycopg2, django-allauth as mentioned in django file
To run: python manage.py runserver (after connecting to database)
Go to admin page and upload csv files 
Now you can enter as student/teacher (on the same page with url '/student' )

Note : Roll numbers are identified as students and other mail-ids are identified as teachers (refer csv file)

Note : Even if some teachers are not willing to use this, others can use it since it does not change their schedule. So, cooperation of everyone is not required and we can scale up the implementation step by step.

Once change is made, the data will be updated in the central database so that no clashes will occur for other batches

**Future Plans**
Teaher and student both need to agree to make a change
Send notification to the teacher and student once a change is made
The teacher can appoint the CR from the website for that course (for the timetable purpose)
If students’ vote is required for a change, it can be included. Then decisions can be made based on that
If a change has happened, the concerned teachers/CR can be notified because some new opportunities might arise due to the change. (If teacher A has made a change, all CRs of those students who have the teacher will receive notification)
We can save history to revert changes
The current database is made to conserve space since timetable changes are not frequent. We can optimize it to make it better.

****

