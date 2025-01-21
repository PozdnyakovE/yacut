from random import choice
import re

from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import YaCutForm
from .models import URLMap
from settings import (ALLOWED_SYMBOLS_FOR_CUSTOM_ID, HOST_ADDRESS,
                      URL_PATTERN)


def get_unique_short_id():
    return ''.join(choice(ALLOWED_SYMBOLS_FOR_CUSTOM_ID) for _ in range(6))


@app.route('/', methods=['GET', 'POST'])
def get_short_url():
    form = YaCutForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if short == '' or short is None:
            short = get_unique_short_id()
        if URLMap.query.filter_by(short=short).first() is not None:
            flash(
                'Предложенный вариант короткой ссылки уже существует.',
                'bad_input'
            )
            return render_template('main_page.html', form=form)
        if re.match(URL_PATTERN, form.original_link.data) is None:
            flash(
                'Оригинальная ссылка содержит ошибку.',
                'bad_input'
            )
            return render_template('main_page.html', form=form)
        url = URLMap(
            original=form.original_link.data,
            short=short
        )
        db.session.add(url)
        db.session.commit()
        flash(f'{HOST_ADDRESS}{url.short}', 'short_link')
    return render_template('main_page.html', form=form)


@app.route('/<short>')
def redirect_to_original_link(short):
    link = URLMap.query.filter_by(short=short).first()
    if link is None:
        abort(404)
    return redirect(link.original)
