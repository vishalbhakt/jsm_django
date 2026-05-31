from django.contrib import admin
from .models import (User, Student, Teacher, Parent, Course, Subject,
                     Assignment, Attendance, Payment, VideoLecture,
                     Announcement, Event, Gallery, Result, Note, Enquiry)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_approved', 'date_joined')
    list_filter = ('role', 'is_approved', 'date_joined')
    search_fields = ('username', 'email')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'created_at')
    list_filter = ('course',)
    search_fields = ('name',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'qualification', 'experience_years')
    search_fields = ('user__username', 'user__email')
    filter_horizontal = ('subjects',)

    def get_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_name.short_description = 'Teacher Name'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'course', 'roll_number')
    list_filter = ('course',)
    search_fields = ('user__username', 'user__email', 'roll_number')

    def get_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_name.short_description = 'Student Name'


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'due_date')
    list_filter = ('subject', 'created_at')
    search_fields = ('title',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('get_student', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('student__user__username',)

    def get_student(self, obj):
        return obj.student.user.get_full_name() or obj.student.user.username
    get_student.short_description = 'Student'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('get_student', 'amount', 'status', 'due_date')
    list_filter = ('status', 'due_date')
    search_fields = ('student__user__username',)

    def get_student(self, obj):
        return obj.student.user.get_full_name() or obj.student.user.username
    get_student.short_description = 'Student'


@admin.register(VideoLecture)
class VideoLectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'created_at')
    list_filter = ('subject', 'created_at')
    search_fields = ('title',)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'audience', 'author', 'created_at')
    list_filter = ('audience', 'created_at')
    search_fields = ('title',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location')
    list_filter = ('date',)
    search_fields = ('title',)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title',)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('get_student', 'subject', 'marks_obtained', 'total_marks', 'percentage')
    list_filter = ('subject', 'exam_name')
    search_fields = ('student__user__username',)

    def get_student(self, obj):
        return obj.student.user.get_full_name() or obj.student.user.username
    get_student.short_description = 'Student'


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'created_at')
    list_filter = ('subject', 'created_at')
    search_fields = ('title',)


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'parent_name', 'class_applied', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('student_name', 'parent_name', 'phone')
