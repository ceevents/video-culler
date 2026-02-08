"""
Test script for video export modules.
Generates sample exports for FCPXML, Premiere, and DaVinci Resolve.
"""

import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from export.fcpxml import export_fcpxml
from export.premiere import export_premiere
from export.davinci import export_davinci_edl, export_davinci_xml


def create_sample_data():
    """Create sample timeline data for testing."""
    return {
        "clips": [
            {
                "path": "/Users/videographer/Wedding_2024/Ceremony_001.mp4",
                "in_point": 5.2,
                "out_point": 15.8,
                "score": 92,
                "category": "ceremony"
            },
            {
                "path": "/Users/videographer/Wedding_2024/FirstDance_001.mp4",
                "in_point": 2.0,
                "out_point": 12.5,
                "score": 88,
                "category": "reception"
            },
            {
                "path": "/Users/videographer/Wedding_2024/Toast_001.mp4",
                "in_point": 0.5,
                "out_point": 8.3,
                "score": 85,
                "category": "reception"
            },
            {
                "path": "/Users/videographer/Wedding_2024/BrideGroom_001.mp4",
                "in_point": 3.0,
                "out_point": 10.0,
                "score": 95,
                "category": "portraits"
            }
        ],
        "markers": [
            {
                "time": 7.5,
                "name": "Music Beat",
                "color": "blue",
                "note": "Sync to music"
            },
            {
                "time": 18.2,
                "name": "Emotional Moment",
                "color": "red",
                "note": "Bride tears"
            },
            {
                "time": 25.0,
                "name": "Key Frame",
                "color": "green"
            }
        ],
        "settings": {
            "framerate": 23.976,
            "resolution": [1920, 1080]
        }
    }


def test_fcpxml():
    """Test FCPXML export."""
    print("\n=== Testing FCPXML Export ===")
    
    data = create_sample_data()
    output_path = "/tmp/video_culler_test_fcpxml.fcpxml"
    
    try:
        result = export_fcpxml(data, output_path)
        print(f"✅ FCPXML export successful: {result}")
        
        # Read and display first few lines
        with open(result, 'r') as f:
            lines = f.readlines()[:20]
            print("\nFirst 20 lines of FCPXML:")
            print("".join(lines))
        
        # Validate XML structure
        import xml.etree.ElementTree as ET
        tree = ET.parse(result)
        root = tree.getroot()
        
        print(f"\n✅ XML is valid")
        print(f"   Root element: {root.tag}")
        print(f"   Version: {root.get('version')}")
        
        # Count clips
        clips = root.findall(".//asset-clip")
        print(f"   Clips found: {len(clips)}")
        
        # Count markers
        markers = root.findall(".//marker")
        print(f"   Markers found: {len(markers)}")
        
    except Exception as e:
        print(f"❌ FCPXML export failed: {e}")
        import traceback
        traceback.print_exc()


def test_premiere():
    """Test Premiere Pro XML export."""
    print("\n=== Testing Premiere Pro XML Export ===")
    
    data = create_sample_data()
    output_path = "/tmp/video_culler_test_premiere.xml"
    
    try:
        result = export_premiere(data, output_path)
        print(f"✅ Premiere XML export successful: {result}")
        
        # Read and display first few lines
        with open(result, 'r') as f:
            lines = f.readlines()[:25]
            print("\nFirst 25 lines of Premiere XML:")
            print("".join(lines))
        
        # Validate XML structure
        import xml.etree.ElementTree as ET
        tree = ET.parse(result)
        root = tree.getroot()
        
        print(f"\n✅ XML is valid")
        print(f"   Root element: {root.tag}")
        print(f"   Version: {root.get('version')}")
        
        # Count clips
        clips = root.findall(".//clipitem")
        print(f"   Clip items found: {len(clips)}")
        
        # Count markers
        markers = root.findall(".//marker")
        print(f"   Markers found: {len(markers)}")
        
    except Exception as e:
        print(f"❌ Premiere XML export failed: {e}")
        import traceback
        traceback.print_exc()


def test_davinci_edl():
    """Test DaVinci Resolve EDL export."""
    print("\n=== Testing DaVinci Resolve EDL Export ===")
    
    data = create_sample_data()
    output_path = "/tmp/video_culler_test_davinci.edl"
    
    try:
        result = export_davinci_edl(data, output_path)
        print(f"✅ DaVinci EDL export successful: {result}")
        
        # Read and display content
        with open(result, 'r') as f:
            content = f.read()
            print("\nEDL Content:")
            print(content)
        
        # Validate EDL format
        lines = content.split('\n')
        
        # Check header
        assert lines[0].startswith("TITLE:"), "Missing TITLE line"
        assert lines[1].startswith("FCM:"), "Missing FCM line"
        
        # Count events
        events = [l for l in lines if l and l[0].isdigit()]
        print(f"\n✅ EDL is valid")
        print(f"   Events found: {len(events)}")
        
    except Exception as e:
        print(f"❌ DaVinci EDL export failed: {e}")
        import traceback
        traceback.print_exc()


def test_davinci_xml():
    """Test DaVinci Resolve XML export."""
    print("\n=== Testing DaVinci Resolve XML Export ===")
    
    data = create_sample_data()
    output_path = "/tmp/video_culler_test_davinci.xml"
    
    try:
        result = export_davinci_xml(data, output_path)
        print(f"✅ DaVinci XML export successful: {result}")
        
        # Read and display first few lines
        with open(result, 'r') as f:
            lines = f.readlines()[:20]
            print("\nFirst 20 lines of DaVinci XML:")
            print("".join(lines))
        
        # Validate XML structure
        import xml.etree.ElementTree as ET
        tree = ET.parse(result)
        root = tree.getroot()
        
        print(f"\n✅ XML is valid")
        print(f"   Root element: {root.tag}")
        print(f"   Version: {root.get('version')}")
        
        # Count clips
        clips = root.findall(".//clipitem")
        print(f"   Clip items found: {len(clips)}")
        
    except Exception as e:
        print(f"❌ DaVinci XML export failed: {e}")
        import traceback
        traceback.print_exc()


def test_different_framerates():
    """Test exports with different frame rates."""
    print("\n=== Testing Different Frame Rates ===")
    
    framerates = [23.976, 24, 29.97, 30, 60]
    
    for fps in framerates:
        print(f"\nTesting {fps} fps...")
        
        data = create_sample_data()
        data["settings"]["framerate"] = fps
        
        try:
            # Test FCPXML
            fcpxml_path = f"/tmp/test_{fps}_fps.fcpxml"
            export_fcpxml(data, fcpxml_path)
            print(f"  ✅ FCPXML @ {fps} fps")
            
            # Test Premiere
            premiere_path = f"/tmp/test_{fps}_fps_premiere.xml"
            export_premiere(data, premiere_path)
            print(f"  ✅ Premiere XML @ {fps} fps")
            
            # Test DaVinci EDL
            edl_path = f"/tmp/test_{fps}_fps.edl"
            export_davinci_edl(data, edl_path)
            print(f"  ✅ DaVinci EDL @ {fps} fps")
            
        except Exception as e:
            print(f"  ❌ Failed at {fps} fps: {e}")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Video Culler Export Module Test Suite")
    print("=" * 60)
    
    test_fcpxml()
    test_premiere()
    test_davinci_edl()
    test_davinci_xml()
    test_different_framerates()
    
    print("\n" + "=" * 60)
    print("Test suite complete!")
    print("=" * 60)
    print("\nGenerated test files in /tmp/:")
    print("  - video_culler_test_fcpxml.fcpxml")
    print("  - video_culler_test_premiere.xml")
    print("  - video_culler_test_davinci.edl")
    print("  - video_culler_test_davinci.xml")
    print("  - test_*_fps.* (various frame rates)")


if __name__ == "__main__":
    main()
