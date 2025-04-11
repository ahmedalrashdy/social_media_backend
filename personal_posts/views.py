# posts/views.py

from rest_framework import generics, permissions
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from utils.permissions.is_author_or_read_only import IsAuthorOrReadOnly
from utils.redis_client import redis_conn
from .models import PersonalPost, PPostInteraction
from .tasks import update_ppost_interaction_db
from rest_framework import  status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import PersonalPost
from .serializers import PersonalPostCreateUpdateSerializer, PersonalPostSerializer
from rest_framework import generics

class PersonalPostCreateView(generics.CreateAPIView):

    queryset = PersonalPost.objects.all()
    serializer_class = PersonalPostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    output_serializer_class = PersonalPostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        instance = serializer.instance

        output_serializer = self.output_serializer_class(instance, context=self.get_serializer_context())

        headers = self.get_success_headers(output_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PersonalPostUpdateView(generics.UpdateAPIView):
    queryset = PersonalPost.objects.all()
    serializer_class = PersonalPostCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    output_serializer_class = PersonalPostSerializer

    def update(self, request, *args, **kwargs):
    
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

      

        output_serializer = self.output_serializer_class(instance, context=self.get_serializer_context())

        return Response(output_serializer.data)


class PersonalPostDeleteView(generics.DestroyAPIView):
    queryset = PersonalPost.objects.all()
    serializer_class = PersonalPostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]


class PersonalPostRetrieveView(generics.RetrieveAPIView):
    queryset = PersonalPost.objects.all()
    serializer_class = PersonalPostSerializer 
    permission_classes = [IsAuthenticated]


class PersonalPostListView(generics.ListAPIView):
    queryset = PersonalPost.objects.all() 
    serializer_class = PersonalPostSerializer
    permission_classes = [IsAuthenticated]





class PersonalPostInteractView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(PersonalPost, id=post_id)
        user = request.user
        interaction_type = request.data.get('type')  

        if interaction_type not in [PPostInteraction.InteractionType.LIKE, PPostInteraction.InteractionType.DISLIKE]:
            return Response({"error": "Invalid interaction type"}, status=status.HTTP_400_BAD_REQUEST)

        if not redis_conn:
            return Response({"error": "Interaction service temporarily unavailable"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        current_interaction = PPostInteraction.objects.filter(
            user=user, post=post).first()
        current_type = current_interaction.type if current_interaction else None

        redis_pipeline = redis_conn.pipeline()
        db_action = None  # ما يجب أن يفعله العامل الخلفي: 'LK', 'DL', أو None للحذف

        # --- الخطوة 2: تحديد التغييرات في Redis وقاعدة البيانات ---
        if current_type == interaction_type:
            # المستخدم يضغط على نفس الزر مرة أخرى -> إلغاء التفاعل
            if interaction_type == PPostInteraction.InteractionType.LIKE:
                redis_pipeline.decr(f"personal_post:{post_id}:likes")
            else:  # Dislike
                redis_pipeline.decr(f"personal_post:{post_id}:dislikes")
            db_action = None  # يعني حذف السجل
        else:
            # تفاعل جديد أو تغيير التفاعل
            if interaction_type == PPostInteraction.InteractionType.LIKE:
                redis_pipeline.incr(f"personal_post:{post_id}:likes")
                if current_type == PPostInteraction.InteractionType.DISLIKE:
                    # كان dislike وأصبح like -> انقص عداد dislike
                    redis_pipeline.decr(f"personal_post:{post_id}:dislikes")
                db_action = PPostInteraction.InteractionType.LIKE
            else:  # Dislike
                redis_pipeline.incr(f"personal_post:{post_id}:dislikes")
                if current_type == PPostInteraction.InteractionType.LIKE:
                    # كان like وأصبح dislike -> انقص عداد like
                    redis_pipeline.decr(f"personal_post:{post_id}:likes")
                db_action = PPostInteraction.InteractionType.DISLIKE

        try:
            redis_pipeline.execute()
        except Exception as e:
            print(f"Redis pipeline execution failed: {e}")
            # return Response({"error": "Failed to update counters"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        update_ppost_interaction_db.delay(
            str(user.id), str(post.id), db_action)

        return Response({
            "status": "success"
        }, status=status.HTTP_200_OK)








# --- Comments ---
class PersonalPostCommentCreateAPIView(generics.CreateAPIView):
    queryset = PersonalPostComment.objects.all()
    serializer_class = PersonalPostCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# --- Replies ---
class PersonalCommentReplyCreateAPIView(generics.CreateAPIView):
    queryset = PersonalCommentReply.objects.all()
    serializer_class = PersonalCommentReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class PCommentInteractionCreateAPIView(generics.CreateAPIView):
    queryset = PCommentInteraction.objects.all()
    serializer_class = PCommentInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PReplayInteractionCreateAPIView(generics.CreateAPIView):
    queryset = PReplayInteraction.objects.all()
    serializer_class = PReplayInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# --- Attachments ---
class PPostAttachmentCreateAPIView(generics.CreateAPIView):
    queryset = PPostAttachment.objects.all()
    serializer_class = PPostAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]



