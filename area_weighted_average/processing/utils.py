import os
import pickle
import requests
import time
import xml.etree.ElementTree as ET

import processing
import requests
from area_weighted_average.processing.config import PLUGIN_VERSION, PROFILE_DICT, MESSAGE_URL
from qgis.core import (
    Qgis,
    QgsApplication,
    QgsCoordinateTransformContext,
    QgsDistanceArea,
    QgsGeometry,
    QgsProcessing,
    QgsProcessingException,
    QgsVectorLayer,
)
from qgis.PyQt.QtWidgets import QPushButton
from qgis.utils import iface

qgis_settings_path = QgsApplication.qgisSettingsDirPath().replace("\\", "/")
awa_log_path = os.path.join(qgis_settings_path, "area_weighted_average.log")
awa_pickle_path = os.path.join(qgis_settings_path, "area_weighted_average.p")
awa_msg_path = os.path.join(qgis_settings_path, "area_weighted_average_msg.html")
awa_msg_cache_duration = 24 * 60 * 60  # 24 hours in seconds


def fetchMessage(url, timeout=2) -> str:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text


def saveToCache(message):
    with open(awa_msg_path, "w") as file:
        file.write(message)


def isCacheValid():
    if os.path.exists(awa_msg_path):
        file_timestamp = os.path.getmtime(awa_msg_path)
        if time.time() - file_timestamp < awa_msg_cache_duration:
            return True
    return False


def loadMessageFromCache():
    if isCacheValid():
        with open(awa_msg_path, "r") as file:
            text = file.read()
            return text
    return ""


def getAndUpdateMessage():
    cached_message = loadMessageFromCache()
    if cached_message:
        return cached_message

    fetched_message = fetchMessage(MESSAGE_URL)
    saveToCache(fetched_message)
    return fetched_message


def incrementUsageCounter() -> int:
    if os.path.exists(awa_pickle_path):  # update existing profile json
        with open(awa_pickle_path, "rb") as f:
            # Reading from json file
            try:  # try and except to handle case where user maanually manipulate awa_pickel file content
                profile_data = pickle.load(f)
                profile_data["usage_counter"] += 1
            except:
                profile_data = PROFILE_DICT.copy()

        with open(awa_pickle_path, "wb") as f:
            pickle.dump(profile_data, f)

        return profile_data["usage_counter"]

    else:  # for the first time create file
        with open(awa_pickle_path, "wb") as f:
            profile_data = PROFILE_DICT.copy()
            pickle.dump(profile_data, f)

        return 1


def getRegistrationStatus() -> bool:
    with open(awa_pickle_path, "rb") as f:
        # Reading from json file
        profile_data = pickle.load(f)
        return profile_data["registered"]


def setRegistrationTrue() -> None:
    with open(awa_pickle_path, "rb") as f:
        # Reading from json file
        profile_data = pickle.load(f)
        profile_data["registered"] = True

    with open(awa_pickle_path, "wb") as f:
        pickle.dump(profile_data, f)

    return


def createHTML(outputFile, counter) -> None:
    import codecs

    with codecs.open(outputFile, "w", encoding="utf-8") as f:
        f.write(
            f"""
<html>

<head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
</head>

<body>
    <p style="font-size:21px;line-height: 1.5;text-align:center;"><br>🎉 WOW! You have used the Area Weighted Average
        Plugin <b>{counter}</b>
        times already 🎉.<br />If you would like to get any GIS task automated for your organization please contact me at
        ars.work.ce@gmail.com<br />
        If this plugin has saved your time, please consider making a personal or organizational donation of any value to
        the developer.</p>
    <br>
    <form action="https://www.paypal.com/donate" method="post" target="_top" style="text-align: center;">
        <input type="hidden" name="business" value="T25JMRWJAL5SQ" />
        <input type="hidden" name="item_name" value="For Area Weighted Average" />
        <input type="hidden" name="currency_code" value="USD" />
        <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif" border="0" name="submit"
            title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />
        <img alt="" border="0" src="https://www.paypal.com/en_US/i/scr/pixel.gif" width="1" height="1" />
    </form>
</body>

</html>"""
        )


def displayUsageMessage(counter):
    from tempfile import NamedTemporaryFile

    appeal_file = NamedTemporaryFile("w", suffix=".html", delete=False)
    createHTML(appeal_file.name, counter)

    def openFileInBrowser():
        import webbrowser

        webbrowser.open_new_tab(appeal_file.name)

    widget = getMessageWidget(
        f"🎉 WOW! You have used the Area Weighted Average Plugin {counter} times already 🎉.",
        "View Message",
        openFileInBrowser,
    )
    displayMessageWidget(widget)


def checkPluginUptodate(plugin_name: str):
    # check if new version is available of the plugin
    avail_version = checkAvailPluginVersion(plugin_name)
    version_comp = zip(avail_version.split("."), PLUGIN_VERSION.split("."))
    for level in version_comp:
        if int(level[0]) > int(level[1]):
            widget = getMessageWidget("Newer version of the plugin is available.", "Upgrade", installPlugin)
            displayMessageWidget(widget)
            return
        elif int(level[0]) < int(level[1]):
            break


def checkAvailPluginVersion(plugin_name: str) -> str:
    qgis_version = Qgis.QGIS_VERSION.replace("-", ".").split(".")
    qgis_version = qgis_version[0] + "." + qgis_version[1]

    r = requests.get(f"https://plugins.qgis.org/plugins/plugins.xml?qgis={qgis_version}")

    xml_str = r.text
    root = ET.fromstring(xml_str)

    for plugin in root.findall("pyqgis_plugin"):
        name = plugin.get("name")
        if name == plugin_name:
            experimental = plugin.find("experimental").text
            if experimental == "False":
                return plugin.find("version").text


def installPlugin():
    import pyplugin_installer

    pyplugin_installer.instance().fetchAvailablePlugins(False)
    pyplugin_installer.instance().installPlugin("area_weighted_average")


def getMessageWidget(message, button_text="", button_func=None):
    widget = iface.messageBar().createMessage("Area Weighted Average", message)
    if button_text and button_func:
        button = QPushButton(widget)
        button.setText(button_text)
        button.pressed.connect(button_func)
        widget.layout().addWidget(button)

    return widget


def displayMessageWidget(widget, level: int = 0, duration: int = 10):
    iface.messageBar().pushWidget(widget, level=level, duration=duration)
