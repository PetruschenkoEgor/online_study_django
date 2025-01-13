from django.db import models


class Course(models.Model):
    """ Модель курса """

    title = models.CharField(max_length=250, verbose_name='Название курса', help_text='Введите название курса')
    preview = models.ImageField(upload_to='materials/course/previews', verbose_name='Заставка курса', help_text='Загрузите заставку курса', blank=True, null=True)
    description = models.TextField(verbose_name='Описание курса', help_text='Введите описание курса', blank=True, null=True)

    def __str__(self):

        return self.title

    class Meta:

        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    """ Модель урока """

    title = models.CharField(max_length=250, verbose_name='Название урока', help_text='Введите название урока')
    description = models.TextField(verbose_name='Описание урока', help_text='Введите описание урока', blank=True, null=True)
    preview = models.ImageField(upload_to='materials/lesson/previews', verbose_name='Заставка урока', help_text='Загрузите заставку урока', blank=True, null=True)
    link_to_the_video = models.CharField(max_length=300, verbose_name='Ссылка', help_text='Введите ссылку на видео', blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True, related_name='lessons')

    def __str__(self):

        return self.title

    class Meta:

        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
