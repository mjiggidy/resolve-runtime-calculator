from __future__ import annotations
import typing
import timecode

from ..utils import trim_info
from ..timecodeinput import timecodeinput

if typing.TYPE_CHECKING:
	from .panel_trimoptions import TRTTrimOptionsWidget
	import DaVinciResolveScript as dvrtypes

class TRTTrimOptionsController:

	def __init__(self, project_manager: dvrtypes.ProjectManager, trim_options_widget:TRTTrimOptionsWidget):

		self._project_manager = project_manager
		self._widget = trim_options_widget

		self._ffoa_input_controller = timecodeinput.TRTTimecodeInputController(
			self._project_manager,
			self._widget.trim_head_input(),
			allow_negative=False,
			as_duration=True
		)
		self._lfoa_input_controller = timecodeinput.TRTTimecodeInputController(
			self._project_manager,
			self._widget.trim_tail_input(),
			allow_negative=False,
			as_duration=True
		)


	def set_enabled(self, is_enabled:bool):

		self._widget.use_ffoa_checkbox.SetEnabled(is_enabled)
		self._widget.use_lfoa_checkbox.SetEnabled(is_enabled)

		self._widget.trim_head_input().SetEnabled(is_enabled)
		self._widget.trim_tail_input().SetEnabled(is_enabled)

	def trim_options(self) -> trim_info.TRTTrimOptions:
		"""Collect the currently-set trim options"""

		project_rate = round(self._project_manager.GetCurrentProject().GetSetting("timelineFrameRate"))

		return trim_info.TRTTrimOptions(
			trim_from_head = timecode.Timecode(self.ffoa_trim_text(), rate=project_rate),
			trim_from_tail = timecode.Timecode(self.lfoa_trim_text(), rate=project_rate),
			use_ffoa_marker = self.use_ffoa_marker(),
			use_lfoa_marker = self.use_lfoa_marker(),
		)

	def set_trim_options(self, trim_options:trim_info.TRTTrimOptions):
		"""Set the trim options"""

		self.ffoa_input_controller().set_from_timecode(trim_options.trim_from_head)
		self.lfoa_input_controller().set_from_timecode(trim_options.trim_from_tail)

		self.set_use_ffoa_marker(trim_options.use_ffoa_marker)
		self.set_use_lfoa_marker(trim_options.use_lfoa_marker)

	def ffoa_trim_text(self) -> str:
		"""Return the FFOA trim amount"""

		return self._widget.trim_head_input().Text

	def set_ffoa_trim_text(self, formatted_duration:str):
		"""Set the FFOA trim amount"""

		self._ffoa_input_controller.set_from_string(formatted_duration)

	def lfoa_trim_text(self) -> str:
		"""Return the LFOA trim amount"""

		return self._widget.trim_tail_input().Text

	def set_lfoa_trim_text(self, formatted_duration:str):
		"""Set the LFOA trim amount"""

		self._lfoa_input_controller.set_from_string(formatted_duration)

	def use_ffoa_marker(self) -> bool:
		"""Return the user's FFOA preference"""

		return self._widget.use_ffoa_checkbox().Checked

	def set_use_ffoa_marker(self, use_marker:bool):
		"""Set use FFOA marker"""

		self._widget.use_ffoa_checkbox().Checked = use_marker

	def use_lfoa_marker(self) -> bool:
		"""Return the user's LFOA preference"""

		return self._widget.use_lfoa_checkbox().Checked

	def set_use_lfoa_marker(self, use_marker:bool):
		"""Set use LFOA marker"""

		self._widget.use_lfoa_checkbox().Checked = use_marker

	def ffoa_input_controller(self) -> timecodeinput.TRTTimecodeInputController:

		return self._ffoa_input_controller

	def lfoa_input_controller(self) -> timecodeinput.TRTTimecodeInputController:

		return self._lfoa_input_controller