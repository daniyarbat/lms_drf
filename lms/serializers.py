from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source="lesson_set", many=True, read_only=True)

    def get_lessons_count(self, instance):
        return instance.lesson_set.count()

    class Meta:
        model = Course
        fields = ('title', 'preview', 'description', 'lessons_count', 'lessons')
