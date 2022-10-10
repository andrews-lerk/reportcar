from django.db import models


class FAQ(models.Model):
    question = models.CharField('Вопрос', max_length=1023)
    answer = models.TextField('Ответ')

    def __str__(self):
        return f'{self.question}'


class ReportsViewCounter(models.Model):
    value = models.IntegerField('Значение')
