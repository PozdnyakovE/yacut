from http import HTTPStatus
from re import match

from flask import jsonify, request

from . import app, db
from .error_handlers import URLMapAPIExceptions
from .models import URLMap
from .utils import check_custom_id, get_unique_short_id
from settings import URL_PATTERN


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
    if match(URL_PATTERN, data['url']) is None:
        raise URLMapAPIExceptions('Оригинальная ссылка содержит ошибку.')
    link = URLMap()
    link.original = data['url']
    link.short = data['custom_id']
    db.session.add(link)
    db.session.commit()
    return jsonify(link.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if link is None:
        raise URLMapAPIExceptions(
            'Указанный id не найден', HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': link.to_dict()['url']}), HTTPStatus.OK
