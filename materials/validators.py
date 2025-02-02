import re

from rest_framework.exceptions import ValidationError


# регулярное выражение для проверки ссылок ютуб
youtube_regex = re.compile(r'^https?://(?:www\.)?youtube\.com/.*')


def validate_link(value):
    """ Проверяем ссылку на ресурс(только http://youtube.com) """

    if not youtube_regex.match(value):
        raise ValidationError('Некорректная ссылка. Ссылка может быть только на личное видео с youtube.com')
