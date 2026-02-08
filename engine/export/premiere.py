"""
Premiere Pro XML Export Module
Generate Adobe Premiere Pro XML timeline exports.

Compatible with Premiere Pro CC 2020+
Based on Final Cut Pro 7 XML interchange format.
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import urllib.parse


class PremiereXMLExporter:
    """Generate Premiere Pro compatible XML"""
    
    # Timebase mapping (ticks per second)
    TIMEBASE_MAP = {
        23.976: "24",
        24: "24",
        25: "25",
        29.97: "30",
        30: "30",
        50: "50",
        59.94: "60",
        60: "60"
    }
    
    # NTSC flag (drop-frame timecode)
    NTSC_FRAMERATES = [23.976, 29.97, 59.94]
    
    def __init__(self, data: Dict[str, Any]):
        """
        Initialize Premiere XML exporter.
        
        Args:
            data: Dictionary containing clips, markers, and settings
        """
        self.clips = data.get("clips", [])
        self.markers = data.get("markers", [])
        self.settings = data.get("settings", {})
        
        self.framerate = self.settings.get("framerate", 24)
        self.resolution = self.settings.get("resolution", [1920, 1080])
        
        # Premiere uses ticks (254016000000 per second at 30fps)
        self.timebase = int(self.TIMEBASE_MAP.get(self.framerate, "24"))
        self.ntsc = "TRUE" if self.framerate in self.NTSC_FRAMERATES else "FALSE"
        
    def _seconds_to_frames(self, seconds: float) -> int:
        """Convert seconds to frame count."""
        return int(round(seconds * self.framerate))
    
    def _frames_to_ticks(self, frames: int) -> int:
        """Convert frames to Premiere ticks."""
        # Premiere uses 254016000000 ticks per second for 30fps
        ticks_per_frame = 254016000000 // self.timebase
        return frames * ticks_per_frame
    
    def _seconds_to_ticks(self, seconds: float) -> int:
        """Convert seconds directly to ticks."""
        frames = self._seconds_to_frames(seconds)
        return self._frames_to_ticks(frames)
    
    def export(self, output_path: str) -> str:
        """
        Generate Premiere Pro XML file.
        
        Args:
            output_path: Path to save the XML file
            
        Returns:
            Path to generated file
        """
        # Create root xmeml element
        xmeml = ET.Element("xmeml", version="5")
        
        # Add sequence
        sequence = self._create_sequence(xmeml)
        
        # Write to file with pretty formatting
        xml_str = self._prettify(xmeml)
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(xml_str, encoding="utf-8")
        
        return str(output_file)
    
    def _create_sequence(self, xmeml: ET.Element) -> ET.Element:
        """Create the sequence (timeline) element."""
        sequence = ET.SubElement(xmeml, "sequence")
        
        # Add sequence metadata
        ET.SubElement(sequence, "name").text = "Video Culler Timeline"
        ET.SubElement(sequence, "duration").text = str(self._calculate_total_duration_ticks())
        
        # Add rate (frame rate settings)
        rate = ET.SubElement(sequence, "rate")
        ET.SubElement(rate, "timebase").text = str(self.timebase)
        ET.SubElement(rate, "ntsc").text = self.ntsc
        
        # Add media
        media = ET.SubElement(sequence, "media")
        
        # Add video track
        video = ET.SubElement(media, "video")
        self._add_video_track(video)
        
        # Add audio track (empty for now, but required)
        audio = ET.SubElement(media, "audio")
        self._add_audio_track(audio)
        
        # Add timecode
        timecode = ET.SubElement(sequence, "timecode")
        rate_tc = ET.SubElement(timecode, "rate")
        ET.SubElement(rate_tc, "timebase").text = str(self.timebase)
        ET.SubElement(rate_tc, "ntsc").text = self.ntsc
        ET.SubElement(timecode, "string").text = "00:00:00:00"
        ET.SubElement(timecode, "frame").text = "0"
        ET.SubElement(timecode, "displayformat").text = "DF" if self.ntsc == "TRUE" else "NDF"
        
        return sequence
    
    def _add_video_track(self, video: ET.Element):
        """Add video track with clips."""
        track = ET.SubElement(video, "track")
        
        current_start_ticks = 0
        
        for i, clip in enumerate(self.clips):
            clip_item = self._create_clip_item(track, clip, i, current_start_ticks)
            
            # Update offset for next clip
            duration_seconds = clip["out_point"] - clip["in_point"]
            duration_ticks = self._seconds_to_ticks(duration_seconds)
            current_start_ticks += duration_ticks
    
    def _create_clip_item(self, track: ET.Element, clip: Dict, index: int, start_ticks: int) -> ET.Element:
        """Create a clip item element."""
        clip_path = Path(clip["path"])
        
        in_ticks = self._seconds_to_ticks(clip["in_point"])
        out_ticks = self._seconds_to_ticks(clip["out_point"])
        duration_ticks = out_ticks - in_ticks
        end_ticks = start_ticks + duration_ticks
        
        clipitem = ET.SubElement(track, "clipitem", id=f"clipitem-{index+1}")
        
        # Basic clip info
        ET.SubElement(clipitem, "name").text = clip_path.stem
        ET.SubElement(clipitem, "duration").text = str(duration_ticks)
        
        # Rate
        rate = ET.SubElement(clipitem, "rate")
        ET.SubElement(rate, "timebase").text = str(self.timebase)
        ET.SubElement(rate, "ntsc").text = self.ntsc
        
        # Timeline position
        ET.SubElement(clipitem, "start").text = str(start_ticks)
        ET.SubElement(clipitem, "end").text = str(end_ticks)
        
        # Source in/out points
        ET.SubElement(clipitem, "in").text = str(in_ticks)
        ET.SubElement(clipitem, "out").text = str(out_ticks)
        
        # File reference
        file_elem = ET.SubElement(clipitem, "file", id=f"file-{index+1}")
        ET.SubElement(file_elem, "name").text = clip_path.name
        
        # Pathurl - use file:// URL format
        file_url = clip_path.absolute().as_uri()
        ET.SubElement(file_elem, "pathurl").text = file_url
        
        # Rate for file
        file_rate = ET.SubElement(file_elem, "rate")
        ET.SubElement(file_rate, "timebase").text = str(self.timebase)
        ET.SubElement(file_rate, "ntsc").text = self.ntsc
        
        # Media info
        media = ET.SubElement(file_elem, "media")
        video_media = ET.SubElement(media, "video")
        
        # Video characteristics
        video_char = ET.SubElement(video_media, "samplecharacteristics")
        rate_char = ET.SubElement(video_char, "rate")
        ET.SubElement(rate_char, "timebase").text = str(self.timebase)
        ET.SubElement(rate_char, "ntsc").text = self.ntsc
        ET.SubElement(video_char, "width").text = str(self.resolution[0])
        ET.SubElement(video_char, "height").text = str(self.resolution[1])
        
        # Add markers to this clip
        self._add_markers_to_clip(clipitem, clip, start_ticks, in_ticks)
        
        # Add metadata if available
        if "score" in clip or "category" in clip:
            labels = ET.SubElement(clipitem, "labels")
            if "category" in clip:
                ET.SubElement(labels, "label2").text = clip["category"]
        
        return clipitem
    
    def _add_markers_to_clip(self, clipitem: ET.Element, clip: Dict, clip_start_ticks: int, in_ticks: int):
        """Add markers that fall within this clip's time range."""
        in_time = clip["in_point"]
        out_time = clip["out_point"]
        
        for marker in self.markers:
            marker_time = marker["time"]
            
            # Check if marker falls within this clip
            if in_time <= marker_time <= out_time:
                # Calculate marker position
                marker_ticks = self._seconds_to_ticks(marker_time)
                
                marker_elem = ET.SubElement(clipitem, "marker")
                ET.SubElement(marker_elem, "name").text = marker.get("name", "Marker")
                ET.SubElement(marker_elem, "comment").text = marker.get("note", "")
                ET.SubElement(marker_elem, "in").text = str(marker_ticks)
                ET.SubElement(marker_elem, "out").text = str(marker_ticks + 1)
    
    def _add_audio_track(self, audio: ET.Element):
        """Add empty audio track (required by Premiere)."""
        track = ET.SubElement(audio, "track")
        
        # Add corresponding audio clips
        current_start_ticks = 0
        
        for i, clip in enumerate(self.clips):
            clip_path = Path(clip["path"])
            
            in_ticks = self._seconds_to_ticks(clip["in_point"])
            out_ticks = self._seconds_to_ticks(clip["out_point"])
            duration_ticks = out_ticks - in_ticks
            end_ticks = current_start_ticks + duration_ticks
            
            clipitem = ET.SubElement(track, "clipitem", id=f"audioclip-{i+1}")
            
            ET.SubElement(clipitem, "name").text = clip_path.stem
            ET.SubElement(clipitem, "duration").text = str(duration_ticks)
            
            rate = ET.SubElement(clipitem, "rate")
            ET.SubElement(rate, "timebase").text = str(self.timebase)
            ET.SubElement(rate, "ntsc").text = self.ntsc
            
            ET.SubElement(clipitem, "start").text = str(current_start_ticks)
            ET.SubElement(clipitem, "end").text = str(end_ticks)
            ET.SubElement(clipitem, "in").text = str(in_ticks)
            ET.SubElement(clipitem, "out").text = str(out_ticks)
            
            # Link to same file
            file_elem = ET.SubElement(clipitem, "file", id=f"file-{i+1}")
            
            current_start_ticks += duration_ticks
    
    def _calculate_total_duration_ticks(self) -> int:
        """Calculate total timeline duration in ticks."""
        total_seconds = 0
        for clip in self.clips:
            total_seconds += clip["out_point"] - clip["in_point"]
        
        return self._seconds_to_ticks(total_seconds)
    
    def _prettify(self, elem: ET.Element) -> str:
        """Return a pretty-printed XML string."""
        rough_string = ET.tostring(elem, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        
        # Add XML declaration and DOCTYPE
        xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
        doctype = '<!DOCTYPE xmeml>\n'
        pretty_xml = reparsed.toprettyxml(indent="  ")
        
        # Remove the default XML declaration added by toprettyxml
        if pretty_xml.startswith('<?xml'):
            pretty_xml = pretty_xml.split('\n', 1)[1]
        
        return xml_declaration + doctype + pretty_xml


def export_premiere(data: Dict[str, Any], output_path: str) -> str:
    """
    Export timeline as Premiere Pro XML format.
    
    Args:
        data: Dictionary containing:
            - clips: List of clip dictionaries with path, in_point, out_point, etc.
            - markers: List of marker dictionaries with time, name, color
            - settings: Dict with framerate and resolution
        output_path: Path to save the XML file
        
    Returns:
        Path to the generated XML file
        
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
        >>> export_premiere(data, "timeline.xml")
    """
    exporter = PremiereXMLExporter(data)
    return exporter.export(output_path)
