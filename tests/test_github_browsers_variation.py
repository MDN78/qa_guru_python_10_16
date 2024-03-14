import pytest
from selene import browser


def test_github_desktop(main_browser):
    if main_browser[0] >= 1280:
        browser.open('/')
        browser.element('.HeaderMenu-link--sign-in').click()
    else:
        pytest.skip(reason='Test only for desktop')


def test_github_mobile(main_browser):
    if main_browser[0] < 1280:
        browser.open('/')
        browser.element('a[href="/login"].d-inline-block').click()
    else:
        pytest.skip(reason='Test only for mobile browser')
