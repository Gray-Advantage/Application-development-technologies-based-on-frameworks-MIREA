from datetime import date

from models import Click, Link, User
from models.clicks import (
    count_clicks_by,
    get_clicks_per_day,
    get_top_links,
    iter_link_clicks,
    register_click,
)

CREATED_AT = date(2026, 9, 1)
EXPIRES_AT = date(2026, 10, 1)


def make_link(code="mirea"):
    owner = User(1, "anna", "anna@example.com", CREATED_AT)
    return Link(code, "https://www.mirea.ru/", owner, CREATED_AT, EXPIRES_AT)


def test_click_creation():
    link = make_link()
    click = Click(1, link, date(2026, 9, 2), "telegram")
    assert click.link is link
    assert click.source == "telegram"


def test_register_click_adds_click():
    link = make_link()
    clicks = []
    click = register_click(clicks, link, date(2026, 9, 2), "Telegram")
    assert clicks == [click]
    assert click.source == "telegram"


def test_count_clicks_by_source():
    link = make_link()
    clicks = []
    register_click(clicks, link, date(2026, 9, 2), "vk")
    register_click(clicks, link, date(2026, 9, 3), "vk")
    register_click(clicks, link, date(2026, 9, 3), "email")
    assert count_clicks_by(clicks, "source") == {"vk": 2, "email": 1}


def test_iter_link_clicks_returns_only_link_clicks():
    mirea = make_link("mirea")
    docs = make_link("docs")
    clicks = []
    register_click(clicks, mirea, date(2026, 9, 2))
    register_click(clicks, docs, date(2026, 9, 2))
    assert [click.link for click in iter_link_clicks(clicks, mirea)] == [mirea]


def test_clicks_per_day_for_new_link():
    assert get_clicks_per_day(5, 0) == 5.0


def test_top_links_sorted_by_clicks():
    mirea = make_link("mirea")
    docs = make_link("docs")
    clicks = []
    register_click(clicks, docs, date(2026, 9, 2))
    register_click(clicks, mirea, date(2026, 9, 2))
    register_click(clicks, mirea, date(2026, 9, 3))
    assert get_top_links([docs, mirea], clicks) == [(mirea, 2), (docs, 1)]
