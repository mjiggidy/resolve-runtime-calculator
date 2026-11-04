from __future__ import annotations
import typing
import mediapoolinput

from . import _settings_widget
from ..utils import match_info, marker_info

if typing.TYPE_CHECKING:
	import DaVinciResolveScript as dvrtypes

DEFAULT_FFOA_MARKER_NAME = "FFOA"
DEFAULT_LFOA_MARKER_NAME = "LFOA"

class TRTSettingsController:

	def __init__(self, project_manager:dvrtypes.ProjectManager, settings_widget:_settings_widget.TRTSettingsWindow):

		self._window_widget = settings_widget

		# Set defaults
		self._window_widget.ffoa_marker_editor().PlaceholderText = DEFAULT_FFOA_MARKER_NAME
		self._window_widget.lfoa_marker_editor().PlaceholderText = DEFAULT_LFOA_MARKER_NAME

		self._match_mediapool_input_controller   = mediapoolinput.MPILineEditController(project_manager, self._window_widget.match_mediapool_folder_editor())
		self._exclude_mediapool_input_controller = mediapoolinput.MPILineEditController(project_manager, self._window_widget.exclude_mediapool_folder_editor())

	def register_window_handle(self, window_handle:object):

		window_handle.On[self._window_widget.id()].Close          = self._on_close
		window_handle.On[self._window_widget.match_mediapool_name_editor().ID].TextChanged     = self._on_match_name_changed
		window_handle.On[self._window_widget.match_mediapool_folder_editor()().ID].TextChanged = self._on_match_folder_changed
		window_handle.On[self._window_widget.exclude_mediapool_folder_editor().ID].TextChanged = self._on_exclude_folder_changed

		self._match_mediapool_input_controller.register_window_handle(window_handle)
		self._exclude_mediapool_input_controller.register_window_handle(window_handle)

	# Event handling

	def _on_match_name_changed(self, event:dict):

		self._window_widget._chk_match_name.Checked = bool(event.get("Text",""))

	def _on_match_folder_changed(self, event:dict):

		self._window_widget._chk_match_folder.Checked = bool(event.get("Text",""))

	def _on_exclude_folder_changed(self, event:dict):

		self._window_widget._chk_exclude_folder.Checked = bool(event.get("Text",""))

	def _on_close(self, event:dict):

		event.get("sender").Hide()

	def set_match_options(self, match_options:match_info.TRTLatestMatchOptions):
		"""Set the Latest match options in the editor"""

		self._window_widget.chk_refresh_project().Checked          = match_options.refresh_project
		self._window_widget.match_mediapool_name_editor().Text     = match_options.match_string
		self._window_widget.match_mediapool_folder_editor().Text   = match_options.match_path
		self._window_widget.exclude_mediapool_folder_editor().Text = match_options.ignore_path

	def match_options(self) -> match_info.TRTLatestMatchOptions:
		"""Get the current Latest match options set by the editor"""

		return match_info.TRTLatestMatchOptions(
			refresh_project = self._window_widget.chk_refresh_project().Checked,
			match_string    = self._window_widget.match_mediapool_name_editor().Text                if self._window_widget.match_mediapool_name_enabler().Checked     else "",
			match_path      = self._window_widget.match_mediapool_folder_editor().Text.strip("/")   if self._window_widget.match_mediapool_folder_enabler().Checked   else "",
			ignore_path     = self._window_widget.exclude_mediapool_folder_editor().Text.strip("/") if self._window_widget.exclude_mediapool_folder_enabler().Checked else "",
		)

	def set_marker_options(self, marker_options:marker_info.TRTMarkerOptions):
		"""Set the Marker Options in the editor"""

		self._window_widget.ffoa_marker_editor().Text = marker_options.ffoa_marker_name
		self._window_widget.lfoa_marker_editor().Text = marker_options.lfoa_marker_name

	def marker_options(self) -> marker_info.TRTMarkerOptions:
		"""Get the current Marker Options set by the editor"""

		return marker_info.TRTMarkerOptions(
			ffoa_marker_name = self._window_widget.ffoa_marker_editor().Text or DEFAULT_FFOA_MARKER_NAME,
			lfoa_marker_name = self._window_widget.lfoa_marker_editor().Text or DEFAULT_LFOA_MARKER_NAME
		)