from rest_framework import serializers
from .models import Course, Lesson, CourseSubscription
from lms.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [UrlValidator(url='link')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source="lesson_set", many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    def get_lessons_count(self, instance):
        return instance.lessons.count()

    def get_subscription(self, instance):
        return CourseSubscription.objects.filter(course=instance, user=self.context['request'].user).exists()

    class Meta:
        model = Course
        fields = '__all__'


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseSubscription
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(fields=['course'], queryset=CourseSubscription.objects.all())
        ]
