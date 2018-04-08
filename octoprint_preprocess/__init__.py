# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import octoprint.filemanager
import logging
import re


class PreprocessPlugin(octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.AssetPlugin,
                       octoprint.plugin.TemplatePlugin):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def get_settings_defaults(self):
        return dict(
            searchStr="",
            replaceStr="",
        )

    def get_assets(self):
        return dict(
            # js=["js/PreProcess.js"],
            # css=["css/PreProcess.css"],
            # less=["less/PreProcess.less"]
        )

    def get_update_information(self):
        return dict(
            PreProcess=dict(
                displayName="Preprocess Plugin",
                displayVersion=self._plugin_version,

                type="github_release",
                user="ieatacid",
                repo="OctoPrint-Preprocess",
                current=self._plugin_version,

                pip="https://github.com/ieatacid/OctoPrint-Preprocess/archive/{target_version}.zip"
            )
        )

    class SearchReplace(octoprint.filemanager.util.LineProcessorStream):
        def process_line(self, line):
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.DEBUG)
            search_regex = r"M190 S\d{2}\r\n|M109 S\d{3}\r\n|M104 S\d{3}\r\n"
            replace_string = "; DELETED TEMP: "
            match = re.search(search_regex, line)
            if match:
                line = replace_string + line
                self.logger.debug("SearchReplace.process_line match: " + line)

            return line

    def preprocess_gcode(self, path, file_object, links=None, printer_profile=None, allow_overwrite=True, *args, **kwargs):
        if not octoprint.filemanager.valid_file_type(path, type="gcode"):
            return file_object

        self.logger.debug("preprocess_gcode")
        return octoprint.filemanager.util.StreamWrapper(file_object.filename, self.SearchReplace(file_object.stream()))


__plugin_name__ = "Preprocess Plugin"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = PreprocessPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        "octoprint.filemanager.preprocessor": __plugin_implementation__.preprocess_gcode
    }

