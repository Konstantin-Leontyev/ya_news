# Импортируем datetime, timedelta.
from datetime import datetime, timedelta
# Импортируем настройки проекта, чтобы получить доступ к парамеру пагинации.
from django.conf import settings
# Импортируем класс клиента.
from django.test.client import Client
# Импортируем функцию reverse(), она понадобится для получения адреса страницы.
from django.urls import reverse
# Импортируем модель заметки, чтобы создать экземпляр.
from news.models import News, Comment
# Импортируем библиотеку pytest.
import pytest


@pytest.fixture
# Используем встроенную фикстуру модели пользователей для создания пользователя - Автор.
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
# Используем встроенную фикстуру модели пользователей для создания пользователя - Не автор.
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
# Создаём анонимного клиента.
def anonymous_client():
    # Создаём новый экземпляр клиента, чтобы не менять глобальный.
    client = Client()
    return client


@pytest.fixture
# Создаем клиента Автора.
def author_client(author):  # Вызываем фикстуру автора.
    # Создаём новый экземпляр клиента, чтобы не менять глобальный.
    client = Client()
    client.force_login(author)  # Логиним автора в клиенте.
    return client


@pytest.fixture
# Создаем клиента не автора.
def not_author_client(not_author): # Вызываем фикстуру не автора.
    client = Client()
    client.force_login(not_author)  # Логиним обычного пользователя в клиенте.
    return client


@pytest.fixture
# Создаём объект новости.
def news(author):
    news = News.objects.create(
        title='Тестовая новость',
        text='Просто текст.',
    )
    return news


@pytest.fixture
# Создаём список новостей.
def news_factory(
        author,
        comment
):
    today = datetime.today()
    all_news = [
        News(
            title=f'Тестовая новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
        # Для каждой новости уменьшаем дату на index дней от today,
        # где index - счётчик цикла.
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
# Создаём объект комментарий.
def comment(author, news):
    comment = Comment.objects.create(  # Создаём объект новости.
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
# Словарь формы для создания тестового комментария.
def comment_form_data(author, news):
    return {
        'news': news,
        'author': author,
        'text': 'Новый текст',
    }


@pytest.fixture
# Создаём список комментариев.
def comment_factory(author, news):
    today = datetime.today()
    all_comments = [
        Comment(
            news=news,
            author=author,
            text='Текст комментария',
            created=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
        # Для каждой новости уменьшаем дату на index дней от today,
        # где index - счётчик цикла.
    ]
    Comment.objects.bulk_create(all_comments)


@pytest.fixture
# Фикстура запрашивает другую фикстуру создания заметки.
def news_id_for_args(news):
    # И возвращает кортеж, который содержит slug заметки.
    # На то, что это кортеж, указывает запятая в конце выражения.
    return (news.id,)


@pytest.fixture
# Фикстура запрашивает другую фикстуру создания заметки.
def comment_id_for_args(comment):
    # И возвращает кортеж, который содержит slug заметки.
    # На то, что это кортеж, указывает запятая в конце выражения.
    return (comment.id,)


@pytest.fixture
# Адрес страницы новости.
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
# Адрес страницы удаления комментария.
def comment_delete_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
# Адрес страницы для редактирования комментария.
def comment_edit_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
# Адрес страницы комментариев новости.
def comments_url(detail_url):
    return detail_url + '#comments'

