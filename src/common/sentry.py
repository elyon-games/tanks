import sentry_sdk
import requests
from common.config import getConfig, common_config, getMode
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.threading import ThreadingIntegration

enable: bool = False

def InitSentry():
    global enable
    sentryConfig: dict = common_config.get("sentry", {})
    if sentryConfig.get("enable", True):
        dsn: str = sentryConfig.get("dsn", "")
        pingTestURL = f"https://{dsn.split('@')[1].split('/')[0]}"
        try :
            requests.get(pingTestURL)
            enable = True
        except Exception:
            enable = False

        if enable:
            sentry_sdk.init(
                dsn=dsn,
                debug=common_config.get("ultraDebug", False),
                traces_sample_rate=1.0,
                profiles_sample_rate=1.0,
                release=common_config.get("version", "0.0.0"),
                environment=getMode(),
                integrations=[LoggingIntegration(), ThreadingIntegration()]
            )

def setContext():
    global enable
    if enable:
        pass