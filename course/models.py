from django.db import models
from django.contrib.auth.models import User
# from django.utils import timezone
# Create your models here.

class Course(models.Model):
    course_name = models.CharField(max_length = 100)
    creator_name = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.course_name

class Test(models.Model):
    test_name = models.CharField(max_length = 20)
    duration = models.DurationField(null = False, default = 0)
    fk_course_id = models.ForeignKey(Course, on_delete = models.CASCADE)

    def __str__(self):
        return self.test_name

class Question(models.Model):
    question = models.CharField(max_length = 100)
    answer = models.CharField(max_length = 100)
    option_1 = models.CharField(max_length = 50)
    option_2 = models.CharField(max_length = 50)
    option_3 = models.CharField(max_length = 50)
    option_4 = models.CharField(max_length = 50)
    fk_test_id = models.ForeignKey(Test, on_delete = models.CASCADE)

    def __str__(self):
        return self.question

class SelectedAnswer(models.Model):
    fk_user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    fk_test_id = models.ForeignKey(Test, on_delete = models.CASCADE)
    fk_question_id = models.ForeignKey(Question, on_delete = models.CASCADE)
    answer = models.CharField(max_length = 100)


class TestAppeared(models.Model):
    fk_user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    fk_test_id = models.ForeignKey(Test, on_delete = models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    score = models.IntegerField(default = 0)

