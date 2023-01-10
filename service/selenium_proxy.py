import os
import zipfile

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class SeleniumConnect:
    manifest_json = ''
    background_js = ''

    def __init__(self, proxy_host, proxy_port, proxy_user, proxy_pass):

        self.manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        self.background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (proxy_host, proxy_port, proxy_user, proxy_pass)

    def get_chromedriver(self, use_proxy=False, user_agent=None, code_script=""):
        chrome_options = webdriver.ChromeOptions()
        if use_proxy:
            pluginfile = 'proxy_auth_plugin_{}.zip'.format(code_script)

            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr("manifest.json", self.manifest_json)
                zp.writestr("background.js", self.background_js)
            chrome_options.add_extension(pluginfile)
        if user_agent:
            chrome_options.add_argument('--user-agent=%s' % user_agent)

        chrome_options.add_argument("--headless=chrome")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            chrome_options=chrome_options)
        return driver
