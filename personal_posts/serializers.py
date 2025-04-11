# personal_posts/serializers.py
from rest_framework import serializers
from .models import PersonalPost, PPostInteraction
from utils.redis_client import  redis_conn

class PersonalPostCreateUpdateSerializer(serializers.ModelSerializer):
    class  Meta:
        model=PersonalPost
        fields = ['text']
        

class PersonalPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    user_interaction_type = serializers.SerializerMethodField()

    class Meta:
        model = PersonalPost
        fields = ['id', "author",'author_name', 'text', 'created_at',
                  'likes_count', 'dislikes_count', 'user_interaction_type']
        read_only_fields = [
            'author',
            'created_at',
            'updated_at',
            
        ]

    def get_counts_from_redis(self, obj):
       
        if not redis_conn:
            return 0, 0

        keys = [
            f"personal_post:{obj.id}:likes",
            f"personal_post:{obj.id}:dislikes"
        ]
        try:
            values = redis_conn.mget(keys)
            likes = int(values[0] or 0)
            dislikes = int(values[1] or 0)
            return likes, dislikes
        except Exception as e:
            print(f"Failed to get counts from Redis for post {obj.id}: {e}")
            return 0, 0 # التعامل مع الخطأ

    def get_likes_count(self, obj):
        likes, _ = self.get_counts_from_redis(obj)
        return likes

    def get_dislikes_count(self, obj):
        _, dislikes = self.get_counts_from_redis(obj)
        return dislikes

    def get_user_interaction_type(self, obj):
        # جلب حالة تفاعل المستخدم الحالي من قاعدة البيانات
        user = self.context['request'].user
        if not user or not user.is_authenticated:
            return None # المستخدم غير مسجل الدخول

        try:
            interaction = PPostInteraction.objects.filter(user=user, post=obj).values_list('type', flat=True).first()
            return interaction # سيكون 'LK' أو 'DL' أو None
        except Exception as e:
             # سجل الخطأ
             print(f"Failed to get user interaction type for user {user.id} post {obj.id}: {e}")
             return None # أرجع None في حالة الخطأ
    def create(self, validated_data):
        return super().create(validated_data)
