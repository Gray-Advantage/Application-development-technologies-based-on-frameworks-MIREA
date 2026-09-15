from datetime import date

from models import Link, User
from models.links import (
    add_link,
    filter_available_links,
    find_links,
    find_links_by_owner,
    is_code_free,
    sort_links,
)

TODAY = date(2026, 9, 15)
EXPIRES_AT = date(2026, 10, 15)
URL = "https://www.mirea.ru/education/programmy-obucheniya/"


def make_user(user_id=1, username="anna"):
    return User(
        user_id, username, f"{username}@example.com", date(2026, 9, 1)
    )


def test_link_creation():
    owner = make_user()
    link = Link("mirea", URL, owner, TODAY, EXPIRES_AT)
    assert link.code == "mirea"
    assert link.owner is owner
    assert link.is_active


def test_link_short_url_property():
    link = Link("mirea", URL, make_user(), TODAY, EXPIRES_AT)
    assert link.short_url == "https://sl.mirea/mirea"


def test_link_str_contains_short_url_and_owner():
    link = Link("mirea", URL, make_user(), TODAY, EXPIRES_AT)
    assert "https://sl.mirea/mirea" in str(link)
    assert "anna" in str(link)


def test_add_link_with_custom_code():
    links = []
    link = add_link(links, make_user(), URL, TODAY, code="mirea")
    assert links == [link]
    assert link.code == "mirea"


def test_generated_codes_are_unique():
    links = []
    owner = make_user()
    first_link = add_link(links, owner, URL, TODAY)
    second_link = add_link(links, owner, URL, TODAY)
    assert first_link.code != second_link.code


def test_taken_code_is_not_free():
    links = []
    add_link(links, make_user(), URL, TODAY, code="mirea")
    assert not is_code_free(links, "mirea")


def test_url_without_scheme_is_invalid():
    assert not Link.validate_url("www.mirea.ru")


def test_find_links_ignores_case():
    links = []
    add_link(links, make_user(), URL, TODAY, code="mirea")
    assert find_links(links, "MIREA")


def test_link_is_not_available_after_lifetime():
    link = add_link([], make_user(), URL, TODAY, lifetime_days=30)
    assert not link.is_available(date(2026, 10, 15))


def test_deactivated_link_is_not_available():
    link = add_link([], make_user(), URL, TODAY)
    link.deactivate()
    assert not link.is_available(TODAY)
    assert link.get_state(TODAY) == "отключена"


def test_filter_available_links_skips_deactivated():
    links = []
    owner = make_user()
    active_link = add_link(links, owner, URL, TODAY, code="active")
    disabled_link = add_link(links, owner, URL, TODAY, code="disabled")
    disabled_link.deactivate()
    assert list(filter_available_links(links, TODAY)) == [active_link]


def test_sort_links_by_code():
    links = []
    owner = make_user()
    add_link(links, owner, URL, TODAY, code="zeta")
    add_link(links, owner, URL, TODAY, code="alpha")
    sorted_codes = [link.code for link in sort_links(links, "code")]
    assert sorted_codes == ["alpha", "zeta"]


def test_find_links_by_owner():
    links = []
    anna = make_user(1, "anna")
    ivan = make_user(2, "ivan")
    anna_link = add_link(links, anna, URL, TODAY, code="anna-link")
    add_link(links, ivan, URL, TODAY, code="ivan-link")
    assert find_links_by_owner(links, anna) == [anna_link]
