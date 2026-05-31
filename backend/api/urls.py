from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CustomTokenObtainPairView, RegisterView, ProfileView,
                    UserViewSet, CourseViewSet, SubjectViewSet, StudentViewSet,
                    TeacherViewSet, ParentViewSet, AssignmentViewSet,
                    AttendanceViewSet, PaymentViewSet, VideoLectureViewSet,
                    AnnouncementViewSet, EventViewSet, GalleryViewSet,
                    ResultViewSet, NoteViewSet, EnquiryViewSet, dashboard_stats)
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'parents', ParentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'video-lectures', VideoLectureViewSet)
router.register(r'announcements', AnnouncementViewSet)
router.register(r'events', EventViewSet)
router.register(r'gallery', GalleryViewSet)
router.register(r'results', ResultViewSet)
router.register(r'notes', NoteViewSet)
router.register(r'enquiries', EnquiryViewSet)

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('dashboard/stats/', dashboard_stats, name='dashboard_stats'),
    path('', include(router.urls)),
]
