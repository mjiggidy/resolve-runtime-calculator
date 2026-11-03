"""
Deals with selecting reels.  Only gonna work for meeeee for now!
"""

from __future__ import annotations
import logging, typing

from resolvecommon import folders, formatting
from ..utils import match_info

if typing.TYPE_CHECKING:
	import DaVinciResolveScript as dvrtypes
	
type ParsedVersion = list[str,int]
"""Parsed, comparible version string"""

EMPTY_PART:str = ""

def refresh_project(current_media_pool:dvrtypes.MediaPool):

	logging.getLogger(__name__).info("Refreshing folders...")
	current_media_pool.RefreshFolders()

def get_latest_from_project(current_media_pool:dvrtypes.MediaPool, match_options:match_info.TRTLatestMatchOptions) -> list[dvrtypes.MediaPoolItem]:
	"""Determine the latest things"""

	latest_per_part:dict[str, list[tuple[ParsedVersion, dvrtypes.MediaPoolItem]]] = dict()

	base_folder   = folders.get_folder_from_path(match_options.match_path, current_media_pool.GetRootFolder())  if match_options.match_path else current_media_pool.GetRootFolder()
	ignore_folder = folders.get_folder_from_path(match_options.ignore_path, current_media_pool.GetRootFolder()) if match_options.ignore_path else None

	for item in folders.get_clips_from_folder(base_folder, recursive=True, ignore_folder=ignore_folder):

		match = match_options.match_pattern.search(item.GetName())

		if not match:
			
			logging.getLogger(__name__).debug("Not matched: %s", item.GetName())
			continue

		parsed_part    = match.group("part") if "part" in match.groupdict() else EMPTY_PART

		if "version" in match.groupdict():

			# Return only the latest version for a given part
			
			#parsed_version = [int(v) if v.isdecimal() else v for v in re.split(r"[^0-9]+", match.group("version"))]
			parsed_version = formatting.format_string_for_natural_sort(match.group("version"))	# NOTE: I... guess this would work huh?! Am I crazy?
		
			if parsed_part not in latest_per_part or latest_per_part[parsed_part][0][0] < parsed_version:
				latest_per_part[parsed_part] = [(parsed_version, item)]

		else:

			# No grouping needed as long as it matches
			if EMPTY_PART not in latest_per_part:
				latest_per_part[EMPTY_PART] = []

			latest_per_part[EMPTY_PART].append(([0,0,0], item))

	return [item[1] for items in latest_per_part.values() for item in items]

def get_selected_media_pool_items(current_media_pool:dvrtypes.MediaPool) -> list[dvrtypes.MediaPoolItem]:
	"""Return selected media pool clips"""
	
	return current_media_pool.GetSelectedClips() or []

def focus_media_pool_item(current_media_pool:dvrtypes.MediaPool, media_pool_item:object):
	"""Select a given media pool item"""

	if not current_media_pool.SetSelectedClip(media_pool_item):
		raise RuntimeError(f"Could not focus {media_pool_item.GetName()}")