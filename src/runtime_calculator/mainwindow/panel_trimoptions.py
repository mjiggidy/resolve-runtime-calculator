from __future__ import annotations
import typing

from ..gui.abstract_widget import TRTAbstractWidget

if typing.TYPE_CHECKING:
	import DaVinciResolveScript as dvrtypes

ID_TXT_TRIM_FFOA    = "txt_ffoa"
ID_TXT_TRIM_LFOA    = "txt_lfoa"

class TRTTrimOptionsWidget(TRTAbstractWidget):
	"""View and edit the trim options"""

	def __init__(self, ui_manager:object):

		super().__init__(ui_manager)

		self._lbl_trim_head = self._ui.Label({
			"Weight": 0,
			"MinimumSize": [130, -1],
			"Text": "Trim from each head:"
		})

		self._txt_trim_head = self._ui.LineEdit({
			"Weight": 100,
			"ID": ID_TXT_TRIM_FFOA,
			"MinimumSize": [45, 20],
			"Events": {"EditingFinished": True},
		})

		self._chk_use_ffoa_marker = self._ui.CheckBox({
			"Weight": 0,
			"Text": "Or use FFOA marker",
			"Checked": True,
			"Events": {},
		})

		self._grp_trim_head = self._ui.HGroup([
			self._lbl_trim_head,
			self._txt_trim_head,
			self._ui.HGap({"Weight":0,"MaximumSize":[20,20]}),
			self._chk_use_ffoa_marker,
		])

		self._lbl_trim_tail = self._ui.Label({
			"Weight": 0,
			"MinimumSize": [130, -1],
			"Text": "Trim from each tail:"
		})

		self._txt_trim_tail = self._ui.LineEdit({
			"Weight": 100,
			"ID": ID_TXT_TRIM_LFOA,
			"MinimumSize": [45, 20],
			"Events": {"EditingFinished": True},
		})

		#self._txt_trim_tail.SetAlignment(timecode_alignment)

		self._chk_use_lfoa_marker = self._ui.CheckBox({
			"Weight": 0,
			"Text": "Or use LFOA marker",
			"Checked": True,
			"Events": {},
		})

		self._grp_trim_tail = self._ui.HGroup([
			self._lbl_trim_tail,
			self._txt_trim_tail,
			self._ui.HGap({"Weight":0,"MaximumSize":[20,20]}),
			self._chk_use_lfoa_marker,
		])


		timecode_alignment = self._txt_trim_head.GetAlignment()
		timecode_alignment["AlignLeft"] = False
		timecode_alignment["AlignRight"] = True

		self._txt_trim_head.SetAlignment(timecode_alignment)
		self._txt_trim_tail.SetAlignment(timecode_alignment)

	def layout(self) -> object:

		return self._ui.VGroup([
			self._grp_trim_head,
			self._grp_trim_tail
		])

	def use_ffoa_checkbox(self) -> object:
		return self._chk_use_ffoa_marker

	def use_lfoa_checkbox(self) -> object:
		return self._chk_use_lfoa_marker

	def trim_head_input(self) -> object:
		return self._txt_trim_head

	def trim_tail_input(self) -> object:
		return self._txt_trim_tail