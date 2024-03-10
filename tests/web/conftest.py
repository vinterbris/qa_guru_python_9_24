import os

import pytest
from dotenv import load_dotenv
from selene import browser, have, be
from selenium.webdriver.chrome.options import Options

from notion_tests.models.application import app
from notion_tests.utils import attach
from notion_tests.test_data.data import workspace_name

def pytest_addoption(parser):
    parser.addoption(
        "--context",
        default="local",
        choices=["local", "selenoid"],
    )


@pytest.fixture(scope='session', autouse=True)
def load_env(request):
    context = request.web_config.getoption("--context")
    load_dotenv()
    load_dotenv(dotenv_path=f'.env.{context}')
    print(context)


@pytest.fixture(scope="function", autouse=True)
def browser_management(request):
    context = request.web_config.getoption("--context")
    from config import web_config

    browser.web_config.base_url = web_config.base_url
    browser.web_config.timeout = web_config.timeout
    browser.web_config.window_width = web_config.window_width
    browser.web_config.window_height = web_config.window_height

    options = Options()
    options.page_load_strategy = 'eager'
    browser.web_config.driver_options = options
    # selenoid_capabilities = {
    #     "browserName": "chrome",
    #     "browserVersion": "122.0",
    #     "selenoid:options": {"enableVNC": True, "enableVideo": True},
    # }
    # options.capabilities.update(selenoid_capabilities)
    #
    # login = os.getenv("SELENOID_LOGIN")
    # password = os.getenv("SELENOID_PASSWORD")
    # driver = webdriver.Remote(
    #     command_executor=f"https://{login}:{password}@selenoid.autotests.cloud/wd/hub",
    #     options=options,
    # )
    #
    # browser.config.driver = driver

    yield
    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser, os.getenv('SELENOID_URL'))

    browser.quit()



@pytest.fixture(scope='function')
def delete_current_page():
    yield
    app.main_page.topbar.open_page_options_panel()
    app.main_page.page_options.choose_delete()

@pytest.fixture(scope='function')
def unfavorite_and_delete_current_page():
    yield
    app.main_page.topbar.open_page_options_panel()
    app.main_page.page_options.choose_delete()
    try:
        app.main_page.topbar.unfavorite_page()
    except:
        pass


@pytest.fixture(scope='function')
def unpublish_page():
    yield
    app.main_page.share_menu.unpublish_page()

@pytest.fixture(scope='function')
def archive_teamspace():
    yield
    app.main_page.sidebar.archive_teamspace(workspace_name)