import re
from flask import jsonify, request

from . import app, db
from .error_handlers import URLMapAPIExceptions
from .models import URLMap
from .views import get_unique_short_id
from settings import (ALLOWED_SYMBOLS_FOR_CUSTOM_ID,
                      LINK_IDENTIFIER_MAX_LENGTH, URL_PATTERN)


def check_custom_id(custom_id):
    if len(custom_id) > LINK_IDENTIFIER_MAX_LENGTH:
        return False
    for symbol in custom_id:
        if symbol not in ALLOWED_SYMBOLS_FOR_CUSTOM_ID:
            return False
    return True


@app.route('/api/id/', methods=['POST'])
def api_get_short_link():
    if not request.data:
        raise URLMapAPIExceptions('Отсутствует тело запроса')
    data = request.get_json()
    if 'url' not in data:
        raise URLMapAPIExceptions('\"url\" является обязательным полем!')
    if 'custom_id' not in data:
        data['custom_id'] = get_unique_short_id()
    if not check_custom_id(data['custom_id']):
        raise URLMapAPIExceptions(
            'Указано недопустимое имя для короткой ссылки'
        )
    if URLMap.query.filter_by(
        short=data['custom_id']
    ).first() is not None:
        raise URLMapAPIExceptions(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    if re.match(URL_PATTERN, data['url']) is None:
        raise URLMapAPIExceptions('Оригинальная ссылка содержит ошибку.')
    link = URLMap()
    link.original = data['url']
    link.short = data['custom_id']
    db.session.add(link)
    db.session.commit()
    return jsonify(link.to_dict()), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if link is None:
        raise URLMapAPIExceptions('Указанный id не найден', 404)
    return jsonify({'url': link.to_dict()['url']}), 200
