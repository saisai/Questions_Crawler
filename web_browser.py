import os
import time

from selenium import webdriver
import platform

from selenium.webdriver.common import keys


class WebBrowser:
    def __init__(self, headless, timeout=0, special=0, user_agent="", proxy_socks=""):
        #
        options = webdriver.FirefoxOptions()
        firefox_profile = webdriver.FirefoxProfile()

        options.add_argument("-safe-mode")
        options.add_argument('-incognito')

        if headless:
            options.add_argument('-headless')

        if special:
            self.special_browser(options, firefox_profile)

        if proxy_socks:
            self.proxy_browser(proxy_socks, firefox_profile)

        if user_agent:
            firefox_profile.set_preference("general.useragent.override", user_agent)

        self.disable_automation(options, firefox_profile)

        if platform.system() == "Linux":
            options.binary_location = "/usr/bin/firefox"
            self.browser = webdriver.Firefox(options=options, firefox_profile=firefox_profile, log_path=os.path.devnull)

        elif platform.system() == "Windows":
            self.browser = webdriver.Firefox(options=options, firefox_profile=firefox_profile, log_path=os.path.devnull,
                                             executable_path=r'geckodriver.exe')

        else:
            print("failed to detect system")
            self.browser = None

        if timeout and self.browser:
            self.browser.set_page_load_timeout(timeout)

    def google_searcher(self, url, keyword):
        self.browser.get(url)
        time.sleep(2)
        self.browser.find_element_by_name("q").clear()
        # write search dork
        self.browser.find_element_by_name("q").send_keys("+".join(keyword.split()))
        # press enter
        self.browser.find_element_by_name("q").send_keys(keys.Keys.ENTER)
        # wait till response
        time.sleep(2)

    @staticmethod
    def special_browser(options, firefox_profile):
        options.add_argument("-mute-audio")
        options.add_argument("-disable-media-source")
        firefox_profile.set_preference('permissions.default.stylesheet', 2)
        firefox_profile.set_preference('permissions.default.image', 2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        firefox_profile.set_preference("dom.webnotifications.enabled", False)
        firefox_profile.set_preference('dom.successive_dialog_time_limit', 0)
        firefox_profile.set_preference('media.autoplay.default', 1)
        firefox_profile.set_preference('media.autoplay.allow-muted', False)
        firefox_profile.set_preference("intl.accept_languages", 'locale')

    @staticmethod
    def proxy_browser(proxy_socks, firefox_profile):
        ip, port = proxy_socks.split(":")
        firefox_profile.set_preference("network.proxy.socks", ip)
        firefox_profile.set_preference("network.proxy.socks_port", int(port))
        firefox_profile.set_preference("network.proxy.type", 1)

    @staticmethod
    def disable_automation(options, firefox_profile):
        firefox_profile.set_preference('useAutomationExtension', False)
        options.add_argument('--disable-automation')
        firefox_profile.set_preference("dom.webdriver.enabled", False)

    """def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            var = getattr(self.browser, name)
            if callable(var):
                return var(*args, **kwargs)
            else:
                return var
        return wrapper"""
