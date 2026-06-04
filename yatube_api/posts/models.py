from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def  __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()

    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True # автоматически поставить время
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE, # если удалить пользователя — удалить все его посты
        related_name='posts'
    )

    image = models.ImageField(
        upload_to='posts/',
        null=True,
        blank=True
    )

    group = models.ForeignKey( # это группа, к которой относится пост
        Group,
        on_delete=models.SET_NULL, # если удалить группу — посты останутся
        related_name='posts',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('id',) # по умолчанию сортировать посты по id

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
