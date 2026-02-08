"""
Example Usage: Video Culler Export Module

This script demonstrates how to use the export functions in a real workflow.
"""

from export.fcpxml import export_fcpxml
from export.premiere import export_premiere
from export.davinci import export_davinci_edl, export_davinci_xml


def example_wedding_export():
    """
    Example: Export a wedding video timeline with high-scoring clips.
    """
    
    # Simulate data from Video Culler analysis
    timeline_data = {
        "clips": [
            # Ceremony clips
            {
                "path": "/Volumes/Media/Wedding_Smith_2024/Ceremony/CAM_A_001.mp4",
                "in_point": 12.5,
                "out_point": 28.3,
                "score": 95,
                "category": "ceremony"
            },
            {
                "path": "/Volumes/Media/Wedding_Smith_2024/Ceremony/CAM_B_002.mp4",
                "in_point": 5.0,
                "out_point": 18.7,
                "score": 92,
                "category": "ceremony"
            },
            
            # Reception clips
            {
                "path": "/Volumes/Media/Wedding_Smith_2024/Reception/FirstDance_001.mp4",
                "in_point": 3.2,
                "out_point": 22.8,
                "score": 98,
                "category": "reception"
            },
            {
                "path": "/Volumes/Media/Wedding_Smith_2024/Reception/Toast_001.mp4",
                "in_point": 1.5,
                "out_point": 15.2,
                "score": 88,
                "category": "reception"
            },
            
            # Portrait/B-roll clips
            {
                "path": "/Volumes/Media/Wedding_Smith_2024/BRoll/Rings_001.mp4",
                "in_point": 0.0,
                "out_point": 6.5,
                "score": 90,
                "category": "details"
            },
            {
                "path": "/Volumes/Media/Wedding_Smith_2024/BRoll/Venue_001.mp4",
                "in_point": 2.0,
                "out_point": 10.0,
                "score": 85,
                "category": "establishing"
            }
        ],
        
        "markers": [
            {
                "time": 15.0,
                "name": "Music Drop",
                "color": "blue",
                "note": "Sync to beat"
            },
            {
                "time": 32.5,
                "name": "Kiss",
                "color": "red",
                "note": "Key moment"
            },
            {
                "time": 50.0,
                "name": "Applause",
                "color": "green",
                "note": "Audience reaction"
            },
            {
                "time": 68.2,
                "name": "First Dance Peak",
                "color": "purple",
                "note": "Emotional moment"
            }
        ],
        
        "settings": {
            "framerate": 23.976,  # Cinematic 24p
            "resolution": [3840, 2160]  # 4K
        }
    }
    
    # Export to all formats
    print("Exporting Wedding Timeline...")
    print("=" * 60)
    
    # Final Cut Pro X
    fcpxml_path = "/Volumes/Media/Wedding_Smith_2024/Exports/wedding_timeline.fcpxml"
    result = export_fcpxml(timeline_data, fcpxml_path)
    print(f"✅ FCPXML exported: {result}")
    
    # Adobe Premiere Pro
    premiere_path = "/Volumes/Media/Wedding_Smith_2024/Exports/wedding_timeline_premiere.xml"
    result = export_premiere(timeline_data, premiere_path)
    print(f"✅ Premiere XML exported: {result}")
    
    # DaVinci Resolve (EDL)
    edl_path = "/Volumes/Media/Wedding_Smith_2024/Exports/wedding_timeline.edl"
    result = export_davinci_edl(timeline_data, edl_path)
    print(f"✅ DaVinci EDL exported: {result}")
    
    # DaVinci Resolve (XML)
    davinci_xml_path = "/Volumes/Media/Wedding_Smith_2024/Exports/wedding_timeline_davinci.xml"
    result = export_davinci_xml(timeline_data, davinci_xml_path)
    print(f"✅ DaVinci XML exported: {result}")
    
    print("\n" + "=" * 60)
    print("All exports complete!")
    print("Import these files into your preferred NLE to continue editing.")


def example_multicam_export():
    """
    Example: Export a multi-camera shoot with different frame rates.
    """
    
    timeline_data = {
        "clips": [
            {
                "path": "/Volumes/Media/Concert/CAM_A_001.mp4",
                "in_point": 0.0,
                "out_point": 30.0,
                "score": 95,
                "category": "wide"
            },
            {
                "path": "/Volumes/Media/Concert/CAM_B_001.mp4", 
                "in_point": 5.0,
                "out_point": 25.0,
                "score": 92,
                "category": "medium"
            },
            {
                "path": "/Volumes/Media/Concert/CAM_C_001.mp4",
                "in_point": 10.0,
                "out_point": 40.0,
                "score": 88,
                "category": "closeup"
            }
        ],
        
        "markers": [
            {"time": 15.0, "name": "Chorus", "color": "blue"},
            {"time": 30.0, "name": "Bridge", "color": "green"}
        ],
        
        "settings": {
            "framerate": 60,  # High frame rate for slow motion
            "resolution": [1920, 1080]
        }
    }
    
    print("\nExporting Concert Timeline (60fps)...")
    print("=" * 60)
    
    fcpxml_path = "/tmp/concert_60fps.fcpxml"
    export_fcpxml(timeline_data, fcpxml_path)
    print(f"✅ Exported: {fcpxml_path}")


def example_minimal_export():
    """
    Example: Minimal export with just clips, no markers or metadata.
    """
    
    timeline_data = {
        "clips": [
            {
                "path": "/Users/editor/Videos/clip1.mp4",
                "in_point": 0.0,
                "out_point": 10.0
            },
            {
                "path": "/Users/editor/Videos/clip2.mp4",
                "in_point": 2.0,
                "out_point": 8.0
            }
        ],
        "markers": [],
        "settings": {
            "framerate": 24,
            "resolution": [1920, 1080]
        }
    }
    
    print("\nExporting Minimal Timeline...")
    print("=" * 60)
    
    # Just export to Premiere
    premiere_path = "/tmp/minimal_timeline.xml"
    export_premiere(timeline_data, premiere_path)
    print(f"✅ Exported: {premiere_path}")


if __name__ == "__main__":
    # Run examples
    # Note: File paths are examples - adjust to your actual media locations
    
    print("\n" + "=" * 60)
    print("Video Culler Export Examples")
    print("=" * 60)
    
    # Uncomment to run:
    # example_wedding_export()
    example_multicam_export()
    example_minimal_export()
    
    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60)
    print("\nNote: Adjust file paths in the script to match your media.")
    print("These examples demonstrate the export API structure.")
