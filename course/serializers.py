from rest_framework import serializers
from .models import *

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class SelectedAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectedAnswer
        fields = '__all__'

class TestAppearedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAppeared
        fields = '__all__'