from datetime import date

from links import (
    add_link,
    find_links,
    is_code_free,
    is_link_active,
    is_valid_url,
)

TODAY = date(2026, 9, 15)
URL = "https://www.mirea.ru/education/programmy-obucheniya/"


def test_add_link_with_custom_code():
    links = {}
    add_link(links, URL, TODAY, code="mirea")
    assert links["mirea"]["url"] == URL


def test_generated_codes_are_unique():
    links = {}
    first_link = add_link(links, URL, TODAY)
    second_link = add_link(links, URL, TODAY)
    assert first_link["code"] != second_link["code"]


def test_taken_code_is_not_free():
    links = {}
    add_link(links, URL, TODAY, code="mirea")
    assert not is_code_free(links, "mirea")


def test_url_without_scheme_is_invalid():
    assert not is_valid_url("www.mirea.ru")


def test_find_links_ignores_case():
    links = {}
    add_link(links, URL, TODAY, code="mirea")
    assert find_links(links, "MIREA")


def test_link_is_not_active_after_lifetime():
    links = {}
    link = add_link(links, URL, TODAY, lifetime_days=30)
    assert not is_link_active(link, date(2026, 10, 15))
