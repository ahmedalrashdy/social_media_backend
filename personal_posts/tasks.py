# personal_posts/tasks.py
from celery import shared_task
from django.contrib.auth import get_user_model
import logging

from .models import PersonalPost, PPostInteraction

User = get_user_model()
logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60) # مثال لإعادة المحاولة
def update_ppost_interaction_db(self, user_id_str, post_id_str, db_action):
    try:
        user = User.objects.get(id=user_id_str)
        post = PersonalPost.objects.get(id=post_id_str)

        if db_action in [PPostInteraction.InteractionType.LIKE, PPostInteraction.InteractionType.DISLIKE]:
            interaction, created = PPostInteraction.objects.update_or_create(
                user=user,
                post=post,
                defaults={'type': db_action} 
            )
           
        elif db_action is None:
            # حذف التفاعل الحالي إذا كان موجودًا
            deleted_count, _ = PPostInteraction.objects.filter(user=user, post=post).delete()
        else:
            logger.warning(f"Invalid db_action '{db_action}' received for user {user_id_str}, post {post_id_str}")

    except User.DoesNotExist:
        logger.error(f"User with id {user_id_str} not found. Cannot update interaction.")
    except PersonalPost.DoesNotExist:
        logger.error(f"PersonalPost with id {post_id_str} not found. Cannot update interaction.")

    except Exception as exc:
        logger.error(f"Error updating interaction DB for user {user_id_str}, post {post_id_str}: {exc}")
        # إعادة المحاولة في حالة الأخطاء العامة (مثل مشاكل اتصال DB المؤقتة)
        raise self.retry(exc=exc)