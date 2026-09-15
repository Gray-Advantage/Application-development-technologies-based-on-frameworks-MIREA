from datetime import date

from clicks import (
    count_by_field,
    delete_link_clicks,
    get_clicks_per_day,
    register_click,
)
from links import add_link


def test_register_click_adds_record():
    links = {}
    add_link(links, "https://www.mirea.ru/", date(2026, 9, 1), code="mirea")
    clicks = []
    register_click(links, clicks, "mirea", date(2026, 9, 2), "Telegram")
    assert clicks[0]["source"] == "telegram"


def test_count_clicks_by_code():
    clicks = [{"code": "mirea"}, {"code": "mirea"}, {"code": "docs"}]
    assert count_by_field(clicks, "code") == {"mirea": 2, "docs": 1}


def test_clicks_per_day_for_new_link():
    assert get_clicks_per_day(5, 0) == 5.0


def test_delete_link_clicks_keeps_other_links():
    clicks = [{"code": "mirea"}, {"code": "docs"}, {"code": "mirea"}]
    delete_link_clicks(clicks, "mirea")
    assert clicks == [{"code": "docs"}]
