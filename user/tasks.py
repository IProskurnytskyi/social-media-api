import random
import string

from user.models import Post, Hashtag

from celery import shared_task


@shared_task
def create_post() -> None:
    characters = string.ascii_letters + string.digits + string.punctuation
    text = "".join(random.choice(characters) for _ in range(20))
    hashtags, created = Hashtag.objects.get_or_create(name="cool")
    post = Post.objects.create(text=text, user_id=1)
    post.hashtags.set([hashtags.id])
