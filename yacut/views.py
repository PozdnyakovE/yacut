from re import match

from flask import flash, redirect, render_template

from . import app, db
from .forms import YaCutForm
from .models import URLMap
from .utils import get_unique_short_id
from settings import HOST_ADDRESS, URL_PATTERN


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
        if match(URL_PATTERN, form.original_link.data) is None:
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
    link = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(link.original)
