import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from stack_underflow_app.models import Answer, PostType, Question, Votes

logger = logging.getLogger(__name__)


def __get_post_object(post_type, post_id):
    post_object = None
    if post_type.name == PostType.QUES:
        post_object = Question.objects.get(id=post_id)
    elif post_type.name == PostType.ANS:
        post_object = Answer.objects.get(id=post_id)
    return post_object


@receiver(signal=[post_save], sender=Votes)
def votes_post_save_handler(sender, **kwargs):
    instance = kwargs["instance"]
    post_object = __get_post_object(instance.post_type, instance.post_id)
    author = post_object.author
    old_rep_points = author.reputation_points
    if instance.upvote:
        author.reputation_points = old_rep_points + 10
        author.save(update_fields=["reputation_points"])
        logger.info(msg=f"Rep. points incremented by 10 successfully for author {author}")
    elif instance.downvote:
        if old_rep_points == 0:
            logger.error(msg="Cannot deduct rep. points since User does not have enough rep. points")
            return
        author.reputation_points = old_rep_points - 10
        author.save(update_fields=["reputation_points"])
        logger.info(msg=f"Rep. points decremented by 10 successfully for author {author}")


@receiver(signal=[post_delete], sender=Votes)
def votes_post_delete_handler(sender, **kwargs):
    instance = kwargs["instance"]
    post_object = __get_post_object(instance.post_type, instance.post_id)
    author = post_object.author
    old_rep_points = author.reputation_points
    # Restore rep points
    if instance.upvote:
        author.reputation_points = old_rep_points - 10
        author.save(update_fields=["reputation_points"])
        logger.info(msg=f"Rep. points decremented by 10 successfully for author {author}")
    elif instance.downvote:
        author.reputation_points = old_rep_points + 10
        author.save(update_fields=["reputation_points"])
        logger.info(msg=f"Rep. points incremented by 10 successfully for author {author}")
