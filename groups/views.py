from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions ,generics

from .models import *
from .serializers import *

# permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOnly(BasePermission):
    """
    صلاحية تسمح فقط لصاحب الكيان (المنشور، المجموعة، إلخ) بالتعديل أو الحذف.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True  # السماح بالقراءة للجميع

        # التأكد من أن المستخدم هو صاحب الكيان (نبحث عن خاصية author أو creator)
        if hasattr(obj, 'author'):
            return obj.author == request.user
        if hasattr(obj, 'creator'):
            return obj.creator == request.user
        if hasattr(obj, 'user'):  # مثل Membership أو تفاعل
            return obj.user == request.user

        return False


# # مثال عام قابل لإعادة الاستخدام:
# class GroupListCreateAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         groups = Group.objects.all()
#         serializer = GroupSerializer(groups, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = GroupSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(creator=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class GroupPostCreateAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = GroupPostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(author=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class GroupListCreateAPIView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class GroupRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated,IsOwnerOnly]


# -------- GroupPost --------
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
    CreateAPIView, UpdateAPIView, DestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from .models import GroupPost
from .serializers import GroupPostSerializer
# from .permissions import IsOwnerOrGroupCreator


# عرض كل المنشورات
class GroupPostListAPIView(ListAPIView):
    queryset = GroupPost.objects.all()
    serializer_class = GroupPostSerializer
    permission_classes = [IsAuthenticated]


# # عرض منشور واحد فقط
class GroupPostDetailAPIView(RetrieveAPIView):
    queryset = GroupPost.objects.all()
    serializer_class = GroupPostSerializer
    permission_classes = [IsAuthenticated]


# إنشاء منشور جديد
class GroupPostCreateAPIView(CreateAPIView):
    queryset = GroupPost.objects.all()
    serializer_class = GroupPostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 

# permissions.py
from rest_framework.permissions import BasePermission

class IsOwnerOrGroupCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if hasattr(obj, 'author'):
            return obj.author == user or obj.group.creator == user

        return False


# تعديل منشور (فقط المالك أو منشئ المجموعة)
class GroupPostUpdateAPIView(UpdateAPIView):
    queryset = GroupPost.objects.all()
    serializer_class = GroupPostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrGroupCreator]


# حذف منشور (فقط المالك أو منشئ المجموعة)
class GroupPostDeleteAPIView(DestroyAPIView):
    queryset = GroupPost.objects.all()
    serializer_class = GroupPostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrGroupCreator]


class GroupPostCommentAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    queryset = GroupPostComment.objects.all()
    serializer_class = GroupPostCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = GroupPostCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupCommentReplyAPIView(APIView):
    queryset = GroupCommentReply.objects.all()
    serializer_class = GroupCommentReplySerializer
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GroupCommentReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GPostInteractionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GPostInteractionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GCommentInteractionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GCommentInteractionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GReplayInteractionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GReplayInteractionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GPostAttachmentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GPostAttachmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
