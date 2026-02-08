"""
DaVinci Resolve Export Module
Generate EDL (Edit Decision List) and XML timeline exports for DaVinci Resolve.

Supports:
- CMX 3600 EDL format (industry standard)
- DaVinci Resolve XML format
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any


class DaVinciEDLExporter:
    """Generate CMX 3600 EDL format for DaVinci Resolve"""
    
    def __init__(self, data: Dict[str, Any]):
        """
        Initialize EDL exporter.
        
        Args:
            data: Dictionary containing clips, markers, and settings
        """
        self.clips = data.get("clips", [])
        self.markers = data.get("markers", [])
        self.settings = data.get("settings", {})
        
        self.framerate = self.settings.get("framerate", 24)
        self.resolution = self.settings.get("resolution", [1920, 1080])
        
        # Determine drop-frame vs non-drop-frame
        self.drop_frame = self.framerate in [29.97, 59.94]
    
    def _frames_to_timecode(self, frames: int) -> str:
        """Convert frame count to timecode string (HH:MM:SS:FF)."""
        fps = int(round(self.framerate))
        
        total_seconds = frames / self.framerate
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        frame = int((total_seconds % 1) * fps)
        
        separator = ";" if self.drop_frame else ":"
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}{separator}{frame:02d}"
    
    def _seconds_to_timecode(self, seconds: float) -> str:
        """Convert seconds to timecode string."""
        frames = int(round(seconds * self.framerate))
        return self._frames_to_timecode(frames)
    
    def export(self, output_path: str) -> str:
        """
        Generate EDL file.
        
        Args:
            output_path: Path to save the EDL file
            
        Returns:
            Path to generated file
        """
        lines = []
        
        # EDL Header
        lines.append("TITLE: Video Culler Timeline")
        lines.append(f"FCM: {'DROP FRAME' if self.drop_frame else 'NON-DROP FRAME'}")
        lines.append("")
        
        # Generate events for each clip
        record_tc = 0.0  # Running timecode on timeline
        
        for event_num, clip in enumerate(self.clips, start=1):
            clip_path = Path(clip["path"])
            
            # Source in/out points
            source_in = clip["in_point"]
            source_out = clip["out_point"]
            duration = source_out - source_in
            
            # Record (timeline) in/out points
            record_in = record_tc
            record_out = record_tc + duration
            
            # Format: Event# Reel# Track Type Source_In Source_Out Record_In Record_Out
            # Track: V = Video, A = Audio, B = Both
            # Type: C = Cut
            
            event_line = (
                f"{event_num:03d}  "
                f"{clip_path.stem[:8]:8s} "
                f"V     C        "
                f"{self._seconds_to_timecode(source_in)} "
                f"{self._seconds_to_timecode(source_out)} "
                f"{self._seconds_to_timecode(record_in)} "
                f"{self._seconds_to_timecode(record_out)}"
            )
            lines.append(event_line)
            
            # Add clip name comment
            lines.append(f"* FROM CLIP NAME: {clip_path.name}")
            
            # Add metadata if available
            if "score" in clip:
                lines.append(f"* VIDEO CULLER SCORE: {clip['score']}")
            if "category" in clip:
                lines.append(f"* CATEGORY: {clip['category']}")
            
            # Add source file path
            lines.append(f"* SOURCE FILE: {clip_path.absolute()}")
            
            # Add markers for this clip
            for marker in self.markers:
                marker_time = marker["time"]
                if source_in <= marker_time <= source_out:
                    # Marker relative to clip start
                    relative_time = marker_time - source_in
                    marker_tc = record_in + relative_time
                    marker_name = marker.get("name", "Marker")
                    lines.append(f"* MARKER: {marker_name} AT {self._seconds_to_timecode(marker_tc)}")
            
            lines.append("")
            
            # Update record timecode
            record_tc = record_out
        
        # Write to file
        edl_content = "\n".join(lines)
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(edl_content, encoding="utf-8")
        
        return str(output_file)


class DaVinciXMLExporter:
    """Generate DaVinci Resolve XML format"""
    
    def __init__(self, data: Dict[str, Any]):
        """
        Initialize XML exporter.
        
        Args:
            data: Dictionary containing clips, markers, and settings
        """
        self.clips = data.get("clips", [])
        self.markers = data.get("markers", [])
        self.settings = data.get("settings", {})
        
        self.framerate = self.settings.get("framerate", 24)
        self.resolution = self.settings.get("resolution", [1920, 1080])
    
    def _seconds_to_frames(self, seconds: float) -> int:
        """Convert seconds to frame count."""
        return int(round(seconds * self.framerate))
    
    def export(self, output_path: str) -> str:
        """
        Generate DaVinci Resolve XML file.
        
        Args:
            output_path: Path to save the XML file
            
        Returns:
            Path to generated file
        """
        # Create root xmeml element (DaVinci uses FCP 7 XML format)
        xmeml = ET.Element("xmeml", version="4")
        
        # Add project
        project = ET.SubElement(xmeml, "project")
        ET.SubElement(project, "name").text = "Video Culler Project"
        
        # Add sequence
        sequence = self._create_sequence(project)
        
        # Write to file with pretty formatting
        xml_str = self._prettify(xmeml)
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(xml_str, encoding="utf-8")
        
        return str(output_file)
    
    def _create_sequence(self, project: ET.Element) -> ET.Element:
        """Create the sequence (timeline) element."""
        sequence = ET.SubElement(project, "sequence")
        
        # Add sequence metadata
        ET.SubElement(sequence, "name").text = "Video Culler Timeline"
        ET.SubElement(sequence, "duration").text = str(self._calculate_total_duration_frames())
        
        # Add rate (frame rate settings)
        rate = ET.SubElement(sequence, "rate")
        timebase = int(round(self.framerate))
        ET.SubElement(rate, "timebase").text = str(timebase)
        ET.SubElement(rate, "ntsc").text = "TRUE" if self.framerate in [23.976, 29.97, 59.94] else "FALSE"
        
        # Add media
        media = ET.SubElement(sequence, "media")
        
        # Add video track
        video = ET.SubElement(media, "video")
        self._add_video_track(video)
        
        return sequence
    
    def _add_video_track(self, video: ET.Element):
        """Add video track with clips."""
        format_elem = ET.SubElement(video, "format")
        samplecharacteristics = ET.SubElement(format_elem, "samplecharacteristics")
        
        rate = ET.SubElement(samplecharacteristics, "rate")
        timebase = int(round(self.framerate))
        ET.SubElement(rate, "timebase").text = str(timebase)
        ET.SubElement(rate, "ntsc").text = "TRUE" if self.framerate in [23.976, 29.97, 59.94] else "FALSE"
        
        ET.SubElement(samplecharacteristics, "width").text = str(self.resolution[0])
        ET.SubElement(samplecharacteristics, "height").text = str(self.resolution[1])
        
        # Add track
        track = ET.SubElement(video, "track")
        
        current_start_frames = 0
        
        for i, clip in enumerate(self.clips):
            clip_item = self._create_clip_item(track, clip, i, current_start_frames)
            
            # Update offset for next clip
            duration_seconds = clip["out_point"] - clip["in_point"]
            duration_frames = self._seconds_to_frames(duration_seconds)
            current_start_frames += duration_frames
    
    def _create_clip_item(self, track: ET.Element, clip: Dict, index: int, start_frames: int) -> ET.Element:
        """Create a clip item element."""
        clip_path = Path(clip["path"])
        
        in_frames = self._seconds_to_frames(clip["in_point"])
        out_frames = self._seconds_to_frames(clip["out_point"])
        duration_frames = out_frames - in_frames
        end_frames = start_frames + duration_frames
        
        clipitem = ET.SubElement(track, "clipitem", id=f"clipitem-{index+1}")
        
        # Basic clip info
        ET.SubElement(clipitem, "name").text = clip_path.stem
        ET.SubElement(clipitem, "duration").text = str(duration_frames)
        
        # Rate
        rate = ET.SubElement(clipitem, "rate")
        timebase = int(round(self.framerate))
        ET.SubElement(rate, "timebase").text = str(timebase)
        ET.SubElement(rate, "ntsc").text = "TRUE" if self.framerate in [23.976, 29.97, 59.94] else "FALSE"
        
        # Timeline position
        ET.SubElement(clipitem, "start").text = str(start_frames)
        ET.SubElement(clipitem, "end").text = str(end_frames)
        
        # Source in/out points
        ET.SubElement(clipitem, "in").text = str(in_frames)
        ET.SubElement(clipitem, "out").text = str(out_frames)
        
        # File reference
        file_elem = ET.SubElement(clipitem, "file", id=f"file-{index+1}")
        ET.SubElement(file_elem, "name").text = clip_path.name
        ET.SubElement(file_elem, "pathurl").text = clip_path.absolute().as_uri()
        
        # Add markers
        self._add_markers_to_clip(clipitem, clip)
        
        return clipitem
    
    def _add_markers_to_clip(self, clipitem: ET.Element, clip: Dict):
        """Add markers that fall within this clip's time range."""
        in_time = clip["in_point"]
        out_time = clip["out_point"]
        
        for marker in self.markers:
            marker_time = marker["time"]
            
            if in_time <= marker_time <= out_time:
                relative_time = marker_time - in_time
                marker_frames = self._seconds_to_frames(relative_time)
                
                marker_elem = ET.SubElement(clipitem, "marker")
                ET.SubElement(marker_elem, "name").text = marker.get("name", "Marker")
                ET.SubElement(marker_elem, "comment").text = marker.get("note", "")
                ET.SubElement(marker_elem, "in").text = str(marker_frames)
                ET.SubElement(marker_elem, "out").text = str(marker_frames)
    
    def _calculate_total_duration_frames(self) -> int:
        """Calculate total timeline duration in frames."""
        total_seconds = 0
        for clip in self.clips:
            total_seconds += clip["out_point"] - clip["in_point"]
        
        return self._seconds_to_frames(total_seconds)
    
    def _prettify(self, elem: ET.Element) -> str:
        """Return a pretty-printed XML string."""
        rough_string = ET.tostring(elem, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")


def export_davinci_edl(data: Dict[str, Any], output_path: str) -> str:
    """
    Export timeline as EDL format for DaVinci Resolve.
    
    Args:
        data: Dictionary containing:
            - clips: List of clip dictionaries with path, in_point, out_point, etc.
            - markers: List of marker dictionaries with time, name, color
            - settings: Dict with framerate and resolution
        output_path: Path to save the EDL file
        
    Returns:
        Path to the generated EDL file
        
    Example:
        >>> data = {
        ...     "clips": [{"path": "/path/to/video.mp4", "in_point": 2.5, "out_point": 8.3}],
        ...     "settings": {"framerate": 23.976, "resolution": [1920, 1080]}
        ... }
        >>> export_davinci_edl(data, "timeline.edl")
    """
    exporter = DaVinciEDLExporter(data)
    return exporter.export(output_path)


def export_davinci_xml(data: Dict[str, Any], output_path: str) -> str:
    """
    Export timeline as XML format for DaVinci Resolve.
    
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
        ...     "clips": [{"path": "/path/to/video.mp4", "in_point": 2.5, "out_point": 8.3}],
        ...     "settings": {"framerate": 23.976, "resolution": [1920, 1080]}
        ... }
        >>> export_davinci_xml(data, "timeline.xml")
    """
    exporter = DaVinciXMLExporter(data)
    return exporter.export(output_path)
