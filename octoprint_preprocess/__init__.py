# coding=utf-8
from __future__ import absolute_import


import octoprint.plugin
import octoprint.filemanager
import regex
import logging


class PreprocessPlugin(octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.AssetPlugin,
                       octoprint.plugin.StartupPlugin,
                       octoprint.plugin.TemplatePlugin):

    def get_settings_defaults(self):
        return dict(
            searchReplace=[{'name':'Example','regexp':'M190 S\d{2}\r\n','replaceString':'; DELETED TEMP: $1'}]
        )

    def get_assets(self):
        return dict(
            js=["js/PreProcess.js"],
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

    def on_after_startup(self):
        for key in sorted(self._settings.get(["searchReplace"])):
            self._logger.info("\n    name:%s \n    regexp:%s \n    replaceString:%s" % (key["name"], key["regexp"], key["replaceString"]))

    class SearchReplace(octoprint.filemanager.util.LineProcessorStream):
        def process_line(self, line):
            def displaymatch(match):
                if match is None:
                    return None
                return '                          Match: %r, groups=%r, lastindex=%r' % (match.group(), match.groups(), match.lastindex)

            plugin_settings = octoprint.plugin.PluginSettings(__plugin_implementation__, "PreProcessPlugin")

            for key in sorted(plugin_settings._settings.get(["searchReplace"])):
                match = regex.compile(key["regexp"]).match(line)

                if match:
                    print(displaymatch(match))
                    replaceString = key["replaceString"]
                    pos = replaceString.find("$1")
                    if pos != -1:
                        line = replaceString[:pos] + match.group()
                    else:
                        line = replaceString

                    if line.find("\n") == -1:
                        line += "\r\n"

            return line

    def preprocess_gcode(self, path, file_object, links=None, printer_profile=None, allow_overwrite=True, *args, **kwargs):
        if not octoprint.filemanager.valid_file_type(path, type="gcode"):
            return file_object

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

