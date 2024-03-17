from rest_framework import serializers
from .models import Course, Lesson, CourseSubscription
from lms.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'link', 'course', 'owner', 'price']
        validators = [UrlValidator(url='link')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source="lesson_set", many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    def get_lessons_count(self, instance):
        return instance.lessons.count()

    def get_subscription(self, instance):
        return CourseSubscription.objects.filter(course=instance, owner=self.context['request'].user).exists()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'subscription', 'lessons_count', 'lessons', 'price']


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseSubscription
        fields = '__all__'
        extra_kwargs = {'is_subscribed': {'default': True}}
