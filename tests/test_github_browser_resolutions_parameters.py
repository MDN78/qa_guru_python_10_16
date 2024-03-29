import pytest
from selene import browser
from resources.resolutions import *


@pytest.mark.parametrize('desktop_browser', [HD], indirect=True)
def test_github_desktop(desktop_browser):
    browser.open('/')
    browser.element('.HeaderMenu-link--sign-in').click()


@pytest.mark.parametrize('mobile_browser', [iPHONE_12_PRO], indirect=True)
def test_github_mobile(mobile_browser):
    browser.open('/')
    browser.element('a[href="/login"].d-inline-block').click()
