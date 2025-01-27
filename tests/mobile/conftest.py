import allure
import allure_commons
import pytest
from appium import webdriver
from dotenv import load_dotenv
from selene import browser, support

from project import notion_config
from notion_ui_tests.models.application import app
from notion_ui_tests.utils import attach


@pytest.fixture(scope='function', autouse=True)
def mobile_management(request):
    context = notion_config.context
    from project import mobile_config

    if context == 'remote':
        remote_url = mobile_config.remote_url_bstack
    else:
        remote_url = mobile_config.local_remote_url

    options = mobile_config.to_driver_options(context)
    with allure.step('init app session'):
        browser.config.driver = webdriver.Remote(remote_url, options=options)
        browser.config.timeout = mobile_config.timeout
        browser.config._wait_decorator = support._logging.wait_with(
            context=allure_commons._allure.StepContext
        )

    yield

    attach.add_screenshot(browser)
    attach.add_xml(browser)

    if context == 'remote':
        session_id = browser.driver.session_id

        with allure.step('tear down app session with id' + session_id):
            browser.quit()

        bstack = options.get_capability('bstack:options')
        attach.add_bstack_video(session_id, bstack['userName'], bstack['accessKey'])

    browser.quit()


@pytest.fixture(scope='function')
def delete_created_page():
    yield
    app.mobile_main_page.delete_page_on_page_screen()
