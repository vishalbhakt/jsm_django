from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Count, Avg

from .models import (User, Student, Teacher, Parent, Course, Subject,
                     Assignment, Attendance, Payment, VideoLecture,
                     Announcement, Event, Gallery, Result, Note, Enquiry)
from .serializers import (UserSerializer, RegisterSerializer, StudentSerializer,
                          TeacherSerializer, ParentSerializer, CourseSerializer,
                          SubjectSerializer, AssignmentSerializer, AttendanceSerializer,
                          PaymentSerializer, VideoLectureSerializer, AnnouncementSerializer,
                          EventSerializer, GallerySerializer, ResultSerializer,
                          NoteSerializer, EnquirySerializer)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if not user.is_superuser and not user.is_approved:
            raise Exception('Account pending admin approval.')
        data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# --- Admin-only ViewSets ---

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.role == 'ADMIN'
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        user = self.get_object()
        user.is_approved = True
        user.save()
        return Response({'status': 'approved'})

    @action(detail=False, methods=['get'])
    def pending(self, request):
        pending = User.objects.filter(is_approved=False, is_superuser=False)
        serializer = self.get_serializer(pending, many=True)
        return Response(serializer.data)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().select_related('user', 'course')
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all().select_related('user')
    serializer_class = TeacherSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]


class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [IsAuthenticated]


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all().select_related('subject', 'teacher__user')
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        subject = self.request.query_params.get('subject')
        if subject:
            qs = qs.filter(subject_id=subject)
        return qs


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all().select_related('student__user')
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        student = self.request.query_params.get('student')
        date = self.request.query_params.get('date')
        if student:
            qs = qs.filter(student_id=student)
        if date:
            qs = qs.filter(date=date)
        return qs


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        student = self.request.query_params.get('student')
        if student:
            qs = qs.filter(student_id=student)
        return qs


class VideoLectureViewSet(viewsets.ModelViewSet):
    queryset = VideoLecture.objects.all().select_related('subject', 'teacher__user')
    serializer_class = VideoLectureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        subject = self.request.query_params.get('subject')
        if subject:
            qs = qs.filter(subject_id=subject)
        return qs


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all().order_by('-created_at')
    serializer_class = AnnouncementSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('date')
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]


class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all().order_by('-created_at')
    serializer_class = GallerySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        student = self.request.query_params.get('student')
        if student:
            qs = qs.filter(student_id=student)
        return qs


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all().select_related('subject', 'teacher__user')
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        subject = self.request.query_params.get('subject')
        if subject:
            qs = qs.filter(subject_id=subject)
        return qs


class EnquiryViewSet(viewsets.ModelViewSet):
    queryset = Enquiry.objects.all().order_by('-created_at')
    serializer_class = EnquirySerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Return summary stats for the dashboard based on user role."""
    user = request.user

    if user.is_superuser or user.role == 'ADMIN':
        data = {
            'total_students': Student.objects.count(),
            'total_teachers': Teacher.objects.count(),
            'total_courses': Course.objects.count(),
            'pending_approvals': User.objects.filter(is_approved=False, is_superuser=False).count(),
            'total_enquiries': Enquiry.objects.count(),
            'recent_announcements': AnnouncementSerializer(
                Announcement.objects.order_by('-created_at')[:5], many=True
            ).data,
            'upcoming_events': EventSerializer(
                Event.objects.order_by('date')[:5], many=True
            ).data,
        }
    elif user.role == 'TEACHER':
        teacher = getattr(user, 'teacher_profile', None)
        data = {
            'total_students': Student.objects.count(),
            'my_subjects': SubjectSerializer(
                teacher.subjects.all(), many=True
            ).data if teacher else [],
            'my_assignments': Assignment.objects.filter(teacher=teacher).count() if teacher else 0,
            'recent_announcements': AnnouncementSerializer(
                Announcement.objects.order_by('-created_at')[:5], many=True
            ).data,
        }
    elif user.role == 'STUDENT':
        student = getattr(user, 'student_profile', None)
        if student:
            attendances = student.attendances.all()
            total = attendances.count()
            present = attendances.filter(status='Present').count()
            data = {
                'attendance_total': total,
                'attendance_present': present,
                'attendance_percentage': round(present / total * 100, 1) if total else 0,
                'pending_payments': student.payments.filter(status='Pending').count(),
                'recent_results': ResultSerializer(
                    student.results.order_by('-date')[:5], many=True
                ).data,
                'recent_announcements': AnnouncementSerializer(
                    Announcement.objects.filter(audience__in=['ALL', 'STUDENTS']).order_by('-created_at')[:5],
                    many=True
                ).data,
            }
        else:
            data = {'error': 'Student profile not found'}
    else:
        data = {'message': 'Welcome!'}

    return Response(data)
