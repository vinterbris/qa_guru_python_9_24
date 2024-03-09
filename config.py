import os

import pydantic_settings
from dotenv import load_dotenv

from notion_tests.utils import file
load_dotenv()

class Config(pydantic_settings.BaseSettings):
    timeout: float = 15.0
    mail_wait_timeout: int = 120000

    mail_api_key: str = os.getenv('MAIL_SLURP_API_KEY')
    mail_inbox_id: str = os.getenv('MAIL_SLURP_INBOX_ID')
    notion_api_url: str = os.getenv('API_URL')
    notion_api_key: str = os.getenv('API_KEY')

    # web
    base_url: str = os.getenv('URL')
    window_width: int = 1600
    window_height: int = 1000

    # mobile
    # app: str = os.getenv('APP')
    # app_wait_activity: str = os.getenv('APP_AWAIT_ACTIVITY')
    # platform_name: str = os.getenv('PLATFORM_NAME')
    # platform_version: str = os.getenv('PLATFORM_VERSION')
    # remote_url: str = os.getenv('REMOTE_URL')
    # device_name: str = os.getenv('DEVICE_NAME')

    def to_driver_options(self, context):
        from appium.options.android import UiAutomator2Options
        options = UiAutomator2Options()

        # if context == 'local':
        #
        # elif context = 'selenoid':
        #
        # elif context == 'bstack':
        #     options.set_capability('remote_url', self.remote_url)
        #     options.set_capability('deviceName', self.device_name)
        #     options.set_capability('platformName', self.platform_name)
        #     options.set_capability('platformVersion', self.platform_version)
        #     options.set_capability('appWaitActivity', self.app_wait_activity)
        #     options.set_capability('app', self.app)
        #     options.set_capability(
        #         'bstack:options', {
        #             'projectName': 'First Python project',
        #             'buildName': 'browserstack-build-1',
        #             'sessionName': 'BStack first_test',
        #             'userName': os.getenv('USER_NAME'),
        #             'accessKey': os.getenv('ACCESSKEY'),
        #         },
        #     )
        # elif context == 'local_mobile':
        #     options.set_capability('platformName', self.platform_name)
        #     options.set_capability('remote_url', self.remote_url)
        #     options.set_capability('app', file.abs_path_from_project(self.app))
        #     options.set_capability('appWaitActivity', self.app_wait_activity)

        return options


config = Config()
