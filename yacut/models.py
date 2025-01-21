from datetime import datetime

from . import db
from settings import (HOST_ADDRESS, ORIGINAL_LINK_MAX_LENGTH,
                      SHORT_LINK_MAX_LENGTH)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LINK_MAX_LENGTH), nullable=False)
    short = db.Column(
        db.String(SHORT_LINK_MAX_LENGTH), nullable=False
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=HOST_ADDRESS + self.short,
        )
