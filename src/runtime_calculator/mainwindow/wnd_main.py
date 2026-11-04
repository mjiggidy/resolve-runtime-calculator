"""
Main window GUI
"""
from __future__ import annotations

import typing

from .tree_results import TRTTreeResults
from .panel_treecontrols import TRTTreeControlsWidget
from .panel_about import TRTAboutPanel
from .panel_summary import TRTSummaryPanel

from ..trimoptionseditor import TRTTrimOptionsWidget, TRTTrimOptionsController

from ..gui.abstract_widget import TRTAbstractWidget
from .. import __version__

if typing.TYPE_CHECKING:
	import DaVinciResolveScript as dvrtypes

DEFAULT_WINDOW_TITLE = "Runtime Calculator"

URL_GITHUB     = "https://github.com/mjiggidy/resolve_runtime_calculator"
URL_DONATE     = "https://ko-fi.com/lilbinboy"

ID_WINDOW_MAIN = "com.glowingpixel.runtimecalculator.mainwindow"
ID_BTN_EXPORT  = "export_trt"
ID_BTN_SETTINGS= "btn_main_settings"

class TRTMainWidget(TRTAbstractWidget):
	"""Main window widget"""
	
	def __init__(self,
		project_manager:dvrtypes.ProjectManager, ui_manager:object, /, show_nag_link:bool = True):
		
		self._ui = ui_manager

		self._trim_controls_widget = TRTTrimOptionsWidget(self._ui)
		self._trim_controls_contoller = TRTTrimOptionsController(project_manager, self._trim_controls_widget)

		self._list_controls = TRTTreeControlsWidget(self._ui)

		self._tree_trims = TRTTreeResults(self._ui)
		self._tree_trims.tree().ColumnWidth[0] = 150
		self._tree_trims.tree().ColumnWidth[1] = 75
		self._tree_trims.tree().ColumnWidth[2] = 75
		self._tree_trims.tree().ColumnWidth[3] = 50
		self._tree_trims.tree().ColumnWidth[4] = 50

		self._summary_display = TRTSummaryPanel(self._ui)

		self._btn_export = self._ui.Button({
			"ID": ID_BTN_EXPORT,
			"Text": "Export Results...",
			"Enabled": False,
			"Events": {"Clicked",True},
		})

		self._about_panel = TRTAboutPanel(
			self._ui,
			app_version = __version__,
			url_github  = URL_GITHUB,
			url_donate  = URL_DONATE if show_nag_link else None
		)

		self._btn_settings = self._ui.Button({
			"ID": ID_BTN_SETTINGS,
			"Weight": 0,
			"FixedSize": [16,16],
			"Text": "⚙︎"
		})
	
	def layout(self):
		
		return self._ui.VGroup([
			self._trim_controls_widget.layout(),

			self._ui.Label({"FrameStyle": 4}),

			self._list_controls.layout(),
			self._tree_trims.layout(),
			self._summary_display.layout(),
			self._btn_export,

			self._ui.Label({"FrameStyle": 4}),

			self._ui.HGroup([
				self._about_panel.layout(),
				self._btn_settings
			]),
		])
	
	def tree_results(self) -> TRTTreeResults:
		"""A reference to the trim results tree"""
		
		return self._tree_trims

	def trim_options_controller(self) -> TRTTrimOptionsController:
		"""The Trim Options editor controller"""

		return self._trim_controls_contoller

	def summary_display(self) -> TRTSummaryPanel:
		"""The Summary display panel"""

		return self._summary_display

	def tree_list_controls(self) -> TRTTreeControlsWidget:
		"""Return the add/clear button things"""

		return self._list_controls

	def export_button(self) -> object:
		"""The Export button"""

		return self._btn_export