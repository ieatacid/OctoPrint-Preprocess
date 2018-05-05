/*
 * View model for OctoPrint-Preprocess
 *
 * Author: ieatacid
 * License: AGPLv3
 */
$(function() {
	function PreprocessViewModel(parameters) {
		var self = this;

		self.settingsViewModel = parameters[0];

		self.searchReplace = ko.observableArray([]);

		self.addSearchReplace = function(data) {
			console.log("addSearchReplace: ");
			console.log(data);
			self.searchReplace.push({name: "", regexp: "", replaceString: ""})
		}

		self.removeSearchReplace = function(filter) {
			console.log("removeSearchReplace: ");
			console.log(filter);
			self.searchReplace.remove(filter);
		}

		self.onBeforeBinding = function () {
			console.log("onBeforeBinding");
			// self.searchReplace(self.settingsViewModel.settings.plugins.PreProcess.searchReplace());
			self.searchReplace(self.settingsViewModel.settings.plugins.PreProcess.searchReplace.slice(0));
		};

		self.onSettingsBeforeSave = function () {
			console.log("onSettingsBeforeSave");
			// self.searchReplace(self.settingsViewModel.settings.plugins.PreProcess.searchReplace());
			self.settingsViewModel.settings.plugins.TerminalCommands.controls(self.searchReplace.slice(0));
		};
	}

	OCTOPRINT_VIEWMODELS.push([
		PreprocessViewModel,
		[ "settingsViewModel" ],
		[ "#settings_plugin_PreProcess" ]
	]);
});
