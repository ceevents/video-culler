"""
FCPXML Export Module
Generate Final Cut Pro X XML (FCPXML 1.10) timeline exports.

Reference: https://developer.apple.com/documentation/professional_video_applications/fcpxml_reference
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from fractions import Fraction


class FCPXMLExporter:
    """Generate FCPXML 1.10 format for Final Cut Pro X"""
    
    # Frame rate mapping to FCPXML format strings
    FRAMERATE_MAP = {
        23.976: "24000/1001s",  # 23.976 fps (film)
        24: "24s",              # 24 fps
        25: "25s",              # 25 fps (PAL)
        29.97: "30000/1001s",   # 29.97 fps (NTSC drop-frame)
        30: "30s",              # 30 fps
        50: "50s",              # 50 fps
        59.94: "60000/1001s",   # 59.94 fps
        60: "60s"               # 60 fps
    }
    
    # Marker colors supported by FCP X
    MARKER_COLORS = {
        "red": "Red",
        "orange": "Orange", 
        "yellow": "Yellow",
        "green": "Green",
        "blue": "Blue",
        "purple": "Purple",
        "pink": "Pink"
    }
    
    def __init__(self, data: Dict[str, Any]):
        """
        Initialize FCPXML exporter.
        
        Args:
            data: Dictionary containing clips, markers, and settings
        """
        self.clips = data.get("clips", [])
        self.markers = data.get("markers", [])
        self.settings = data.get("settings", {})
        
        self.framerate = self.settings.get("framerate", 24)
        self.resolution = self.settings.get("resolution", [1920, 1080])
        
        # Calculate frame duration
        self.frame_duration = self._get_frame_duration()
        
    def _get_frame_duration(self) -> str:
        """Get the frame duration string for FCPXML."""
        return self.FRAMERATE_MAP.get(self.framerate, "24s")
    
    def _seconds_to_frames(self, seconds: float) -> int:
        """Convert seconds to frame count."""
        return int(round(seconds * self.framerate))
    
    def _frames_to_timecode(self, frames: int) -> str:
        """Convert frame count to rational time string."""
        return f"{frames}/{int(self.framerate)}s"
    
    def _get_color_name(self, color: str) -> str:
        """Map color name to FCP X color."""
        return self.MARKER_COLORS.get(color.lower(), "Blue")
    
    def export(self, output_path: str) -> str:
        """
        Generate FCPXML file.
        
        Args:
            output_path: Path to save the FCPXML file
            
        Returns:
            Path to generated file
        """
        # Create root element
        fcpxml = ET.Element("fcpxml", version="1.10")
        
        # Add resources section
        resources = ET.SubElement(fcpxml, "resources")
        self._add_resources(resources)
        
        # Add library and event
        library = ET.SubElement(fcpxml, "library")
        event = ET.SubElement(library, "event", name="Video Culler Export")
        
        # Add project (timeline)
        project = self._create_project(event)
        
        # Write to file with pretty formatting
        xml_str = self._prettify(fcpxml)
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(xml_str, encoding="utf-8")
        
        return str(output_file)
    
    def _add_resources(self, resources: ET.Element):
        """Add video file resources."""
        for i, clip in enumerate(self.clips):
            clip_path = Path(clip["path"])
            
            # Create format element
            format_id = f"r{i+1}"
            format_elem = ET.SubElement(
                resources,
                "format",
                id=format_id,
                name=f"{self.resolution[0]}x{self.resolution[1]}p",
                frameDuration=self.frame_duration,
                width=str(self.resolution[0]),
                height=str(self.resolution[1])
            )
            
            # Create asset element
            asset_id = f"r{i+100}"
            asset_elem = ET.SubElement(
                resources,
                "asset",
                id=asset_id,
                name=clip_path.stem,
                src=f"file://{clip_path.absolute()}",
                start="0s",
                hasVideo="1",
                hasAudio="1",
                format=format_id,
                duration=f"{self._seconds_to_frames(clip['out_point'])}s"
            )
            
            # Store IDs for later reference
            clip["_format_id"] = format_id
            clip["_asset_id"] = asset_id
    
    def _create_project(self, event: ET.Element) -> ET.Element:
        """Create the project (timeline) element."""
        project = ET.SubElement(event, "project", name="Video Culler Timeline")
        
        sequence = ET.SubElement(
            project,
            "sequence",
            format=self.clips[0]["_format_id"] if self.clips else "r1",
            duration=self._calculate_total_duration(),
            tcStart="0s",
            tcFormat="NDF" if self.framerate in [24, 30, 60] else "DF"
        )
        
        # Create spine (main timeline)
        spine = ET.SubElement(sequence, "spine")
        
        # Add clips to spine
        current_offset = 0
        for clip in self.clips:
            clip_elem = self._create_clip_element(spine, clip, current_offset)
            
            # Add markers to this clip if any fall within its range
            self._add_markers_to_clip(clip_elem, clip, current_offset)
            
            # Update offset for next clip
            duration = clip["out_point"] - clip["in_point"]
            current_offset += self._seconds_to_frames(duration)
        
        # Add standalone markers (not attached to clips)
        self._add_standalone_markers(spine)
        
        return project
    
    def _create_clip_element(self, spine: ET.Element, clip: Dict, offset: int) -> ET.Element:
        """Create a clip element for the timeline."""
        in_frames = self._seconds_to_frames(clip["in_point"])
        out_frames = self._seconds_to_frames(clip["out_point"])
        duration = out_frames - in_frames
        
        clip_elem = ET.SubElement(
            spine,
            "asset-clip",
            name=Path(clip["path"]).stem,
            ref=clip["_asset_id"],
            offset=self._frames_to_timecode(offset),
            duration=self._frames_to_timecode(duration),
            start=self._frames_to_timecode(in_frames),
            tcFormat="NDF" if self.framerate in [24, 30, 60] else "DF"
        )
        
        # Add metadata for score and category
        if "score" in clip or "category" in clip:
            metadata = ET.SubElement(clip_elem, "metadata")
            
            if "score" in clip:
                ET.SubElement(
                    metadata,
                    "md",
                    key="com.videoCuller.score",
                    value=str(clip["score"])
                )
            
            if "category" in clip:
                ET.SubElement(
                    metadata,
                    "md", 
                    key="com.videoCuller.category",
                    value=clip["category"]
                )
        
        return clip_elem
    
    def _add_markers_to_clip(self, clip_elem: ET.Element, clip: Dict, clip_offset: int):
        """Add markers that fall within this clip's time range."""
        in_time = clip["in_point"]
        out_time = clip["out_point"]
        
        for marker in self.markers:
            marker_time = marker["time"]
            
            # Check if marker falls within this clip
            if in_time <= marker_time <= out_time:
                # Calculate marker position relative to clip start
                relative_time = marker_time - in_time
                relative_frames = self._seconds_to_frames(relative_time)
                
                ET.SubElement(
                    clip_elem,
                    "marker",
                    start=self._frames_to_timecode(relative_frames),
                    value=marker.get("name", "Marker"),
                    completed="0",
                    note=marker.get("note", "")
                )
    
    def _add_standalone_markers(self, spine: ET.Element):
        """Add markers not attached to any specific clip."""
        # This could be used for markers that don't fall within any clip
        pass
    
    def _calculate_total_duration(self) -> str:
        """Calculate total timeline duration."""
        total_frames = 0
        for clip in self.clips:
            duration = clip["out_point"] - clip["in_point"]
            total_frames += self._seconds_to_frames(duration)
        
        return self._frames_to_timecode(total_frames)
    
    def _prettify(self, elem: ET.Element) -> str:
        """Return a pretty-printed XML string."""
        rough_string = ET.tostring(elem, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")


def export_fcpxml(data: Dict[str, Any], output_path: str) -> str:
    """
    Export timeline as FCPXML format for Final Cut Pro X.
    
    Args:
        data: Dictionary containing:
            - clips: List of clip dictionaries with path, in_point, out_point, etc.
            - markers: List of marker dictionaries with time, name, color
            - settings: Dict with framerate and resolution
        output_path: Path to save the FCPXML file
        
    Returns:
        Path to the generated FCPXML file
        
    Example:
        >>> data = {
        ...     "clips": [
        ...         {
        ...             "path": "/path/to/video.mp4",
        ...             "in_point": 2.5,
        ...             "out_point": 8.3,
        ...             "score": 85,
        ...             "category": "ceremony"
        ...         }
        ...     ],
        ...     "markers": [
        ...         {"time": 5.2, "name": "Beat", "color": "blue"}
        ...     ],
        ...     "settings": {
        ...         "framerate": 23.976,
        ...         "resolution": [1920, 1080]
        ...     }
        ... }
        >>> export_fcpxml(data, "timeline.fcpxml")
    """
    exporter = FCPXMLExporter(data)
    return exporter.export(output_path)
