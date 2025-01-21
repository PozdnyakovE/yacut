from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from settings import LINK_IDENTIFIER_MAX_LENGTH, ORIGINAL_LINK_MAX_LENGTH


class YaCutForm(FlaskForm):
    original_link = URLField(
        'Введите оригинальную ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, ORIGINAL_LINK_MAX_LENGTH)]
    )
    custom_id = StringField(
        'Ваш вариант идентификатора',
        validators=[Length(1, LINK_IDENTIFIER_MAX_LENGTH), Optional()]
    )
    submit = SubmitField('Создать')
