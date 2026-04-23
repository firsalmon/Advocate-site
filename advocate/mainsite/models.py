# mainsite/models.py
from django.db import models

class Lead(models.Model):
    name = models.CharField("ФИО", max_length=100)
    phone = models.CharField("Телефон", max_length=20)
    message = models.TextField("Описание дела", blank=True)
    created_at = models.DateTimeField("Дата заявки", auto_now_add=True)
    is_processed = models.BooleanField("Обработана", default=False)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} · {self.phone}"


class Review(models.Model):
    author = models.CharField("Автор", max_length=100)
    text = models.TextField("Текст отзыва")
    case_type = models.CharField("Тип дела", max_length=100, blank=True)
    year = models.CharField("Год", max_length=4, blank=True)
    is_published = models.BooleanField("Опубликован", default=True)
    created_at = models.DateTimeField("Добавлен", auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]

    def __str__(self):
        return self.author


class ThankfulLetter(models.Model):
    title = models.CharField("Заголовок / Краткое описание", max_length=200, blank=True)
    image = models.ImageField("Скан / Фото письма", upload_to="thankful_letters/")
    link = models.URLField("Ссылка на источник (если есть)", blank=True)
    is_published = models.BooleanField("Опубликован", default=True)
    created_at = models.DateTimeField("Добавлен", auto_now_add=True)

    class Meta:
        verbose_name = "Благодарственное письмо"
        verbose_name_plural = "Благодарственные письма"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or f"Письмо #{self.id}"


class Questions(models.Model):
    class Priority(models.IntegerChoices):
        IMPORTANT = 3, "Важный"
        LESS_IMPORTANT = 2, "Менее важный"
        LOW_IMPORTANT = 1, "Не важный"

    question = models.CharField("Вопрос", max_length=200)
    answer = models.TextField("Ответ", max_length=300)
    is_published = models.BooleanField("Опубликован", default=True)
    priority = models.PositiveIntegerField(
        "Приоритет вопроса", 
        choices=Priority.choices,
        default=Priority.LOW_IMPORTANT
    )

    class Meta:
        verbose_name = "Часто задаваемые вопросы"
        verbose_name_plural = "Часто задаваемые вопросы" 
        ordering = ["-priority"]
        indexes = [models.Index(fields=['priority'])]

    def __str__(self):
        return self.question