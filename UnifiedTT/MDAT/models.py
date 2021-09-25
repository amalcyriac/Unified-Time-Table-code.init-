from django.db import models

# Create your models here.
class time_table(models.Model):
    course_id = models.CharField(max_length = 20)
    batch_id = models.CharField(max_length = 20)
    allocation = models.CharField(max_length = 1000)
    class Meta:
        db_table = 'time_table'

class students(models.Model):
    student_id = models.CharField(max_length = 20)
    course_id = models.CharField(max_length = 20)
    batch_id = models.CharField(max_length = 20)

    class Meta:
        db_table = 'student'

class teachers(models.Model):
    teacher_id = models.CharField(max_length = 20)
    course_id = models.CharField(max_length = 20)
    batch_id = models.CharField(max_length = 20)
    cr_id = models.CharField(max_length = 20)

    class Meta:
        db_table = 'teacher'

class courses(models.Model):
    course_id = models.CharField(max_length = 20)
    course_name = models.CharField(max_length = 50)
    slot = models.CharField(max_length = 20)
    class Meta:
        db_table = 'courses'

class slot_time_table(models.Model):
    day = models.CharField(max_length = 20)
    hour1 = models.CharField(max_length = 50)
    hour2 = models.CharField(max_length = 50)
    hour3 = models.CharField(max_length = 50)
    hour4 = models.CharField(max_length = 50)
    hour5 = models.CharField(max_length = 50)
    hour6 = models.CharField(max_length = 50)
    hour7 = models.CharField(max_length = 50)
    hour8 = models.CharField(max_length = 50)
    hour9 = models.CharField(max_length = 50)
    class Meta:
        db_table = 'slot_time_table'
