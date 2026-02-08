# Video Culler Export Module

Professional timeline export for Final Cut Pro X, Adobe Premiere Pro, and DaVinci Resolve.

## Features

✅ **FCPXML 1.10** - Final Cut Pro X timeline export  
✅ **Premiere Pro XML** - Adobe Premiere Pro CC 2020+ compatible  
✅ **DaVinci EDL** - CMX 3600 Edit Decision List format  
✅ **DaVinci XML** - XML timeline for DaVinci Resolve  

### Supported Features

- ✅ Video clips with precise in/out points
- ✅ Markers at beat points and key moments
- ✅ Multiple frame rates (23.976, 24, 25, 29.97, 30, 50, 59.94, 60)
- ✅ Resolution detection (1080p, 4K, custom)
- ✅ Metadata (scores, categories)
- ✅ Drop-frame and non-drop-frame timecode
- ✅ Multiple video tracks (FCPXML)
- ✅ Audio track synchronization

## Installation

No additional dependencies required. Uses Python standard library only.

```bash
cd ~/Projects/video-culler/engine/export
```

## Usage

### Input Format

All export functions accept the same input format:

```python
{
    "clips": [
        {
            "path": "/absolute/path/to/video.mp4",
            "in_point": 2.5,      # seconds
            "out_point": 8.3,      # seconds
            "score": 85,           # optional
            "category": "ceremony" # optional
        }
    ],
    "markers": [
        {
            "time": 5.2,          # seconds (absolute)
            "name": "Beat",
            "color": "blue",      # optional
            "note": "Sync point"  # optional
        }
    ],
    "settings": {
        "framerate": 23.976,      # fps
        "resolution": [1920, 1080] # [width, height]
    }
}
```

### FCPXML Export

Generate Final Cut Pro X timeline (FCPXML 1.10):

```python
from export.fcpxml import export_fcpxml

data = {
    "clips": [...],
    "markers": [...],
    "settings": {"framerate": 23.976, "resolution": [1920, 1080]}
}

output_file = export_fcpxml(data, "timeline.fcpxml")
```

**Import into Final Cut Pro X:**
1. File → Import → XML
2. Select generated `.fcpxml` file
3. Timeline will appear in your event

**Supported versions:** Final Cut Pro X 10.4+

### Premiere Pro Export

Generate Adobe Premiere Pro XML:

```python
from export.premiere import export_premiere

data = {
    "clips": [...],
    "markers": [...],
    "settings": {"framerate": 23.976, "resolution": [1920, 1080]}
}

output_file = export_premiere(data, "timeline.xml")
```

**Import into Premiere Pro:**
1. File → Import
2. Select generated `.xml` file
3. Sequence will appear in Project panel

**Supported versions:** Premiere Pro CC 2020+

### DaVinci Resolve Export

Generate EDL (recommended) or XML:

```python
from export.davinci import export_davinci_edl, export_davinci_xml

# EDL format (recommended - simpler, more reliable)
output_file = export_davinci_edl(data, "timeline.edl")

# XML format (alternative)
output_file = export_davinci_xml(data, "timeline.xml")
```

**Import into DaVinci Resolve:**

**For EDL:**
1. File → Import → Timeline → Import AAF, EDL, XML...
2. Select `.edl` file
3. Timeline will be created

**For XML:**
1. File → Import → Timeline → Import AAF, EDL, XML...
2. Select `.xml` file
3. Choose import options

**Supported versions:** DaVinci Resolve 17+

## Frame Rates

All export formats support these frame rates:

| Frame Rate | Type | Timecode Format |
|------------|------|-----------------|
| 23.976     | Film (NTSC) | Drop-frame |
| 24         | Film | Non-drop-frame |
| 25         | PAL | Non-drop-frame |
| 29.97      | NTSC | Drop-frame |
| 30         | NTSC | Non-drop-frame |
| 50         | PAL | Non-drop-frame |
| 59.94      | High frame rate | Drop-frame |
| 60         | High frame rate | Non-drop-frame |

## Markers

Markers are automatically attached to clips based on their time position:

- FCPXML: Markers appear within clip elements
- Premiere: Markers appear as clip markers
- DaVinci: Markers appear as EDL comments

**Supported marker colors (FCPXML):**
- Red
- Orange
- Yellow
- Green
- Blue (default)
- Purple
- Pink

## Metadata

Custom metadata is preserved:

- **Score** - Video quality score (0-100)
- **Category** - Scene category (ceremony, reception, etc.)

FCPXML stores this in metadata fields:
- `com.videoCuller.score`
- `com.videoCuller.category`

Premiere stores this in clip labels.

## Testing

Run the test suite:

```bash
cd ~/Projects/video-culler/engine/export
python3 test_exports.py
```

Test files are generated in `/tmp/`:
- `video_culler_test_fcpxml.fcpxml`
- `video_culler_test_premiere.xml`
- `video_culler_test_davinci.edl`
- `video_culler_test_davinci.xml`

## File Paths

All file paths in the input data should be **absolute paths**:

```python
# ✅ Good
"path": "/Users/videographer/Wedding_2024/Ceremony_001.mp4"

# ❌ Bad
"path": "Ceremony_001.mp4"
"path": "~/Wedding_2024/Ceremony_001.mp4"
```

The export modules will convert paths to `file://` URLs automatically.

## Timecode Calculations

All time values are in **seconds** (float):

```python
"in_point": 2.5   # 2.5 seconds
"out_point": 8.3  # 8.3 seconds
```

Internal conversions:
- **FCPXML** - Uses rational time (frames/fps)
- **Premiere** - Uses ticks (254016000000 per second @ 30fps)
- **DaVinci EDL** - Uses HH:MM:SS:FF timecode

## Limitations

### FCPXML
- No compound clips (all clips are asset-clips)
- Single spine (main storyline) - no connected clips yet
- Markers must fall within clip boundaries

### Premiere Pro XML
- Based on FCP 7 XML interchange format
- May require media relinking if paths change
- Limited effect support

### DaVinci EDL
- EDL format has limited metadata support
- Clip names are truncated to 8 characters in reel column
- Full paths are stored in comments

### DaVinci XML
- Uses FCP 7 XML format (version 4)
- Simpler than FCPXML but less feature-rich

## Troubleshooting

### "Media Offline" in FCP/Premiere

**Problem:** Clips show as offline/missing  
**Solution:** Ensure file paths are absolute and files exist

### Wrong Frame Rate

**Problem:** Timecode doesn't match  
**Solution:** Verify `framerate` in settings matches source media

### Markers Not Appearing

**Problem:** Markers don't show up  
**Solution:** Check that marker times fall within clip in/out points

### EDL Import Fails in DaVinci

**Problem:** EDL won't import  
**Solution:** Try XML format instead, or check EDL syntax with text editor

## Advanced Usage

### Multiple Tracks (FCPXML only)

To add clips to different video tracks, you can extend the FCPXML module:

```python
# Future feature - not yet implemented
data = {
    "tracks": [
        {"clips": [...]},  # Track 1
        {"clips": [...]}   # Track 2
    ]
}
```

### Transitions

Transitions are not currently supported. All edits are straight cuts.

### Effects

No effects are exported. Only clips and markers.

## API Reference

### `export_fcpxml(data, output_path)`

Generate FCPXML 1.10 timeline.

**Parameters:**
- `data` (dict) - Timeline data (clips, markers, settings)
- `output_path` (str) - Path to save `.fcpxml` file

**Returns:** `str` - Path to generated file

### `export_premiere(data, output_path)`

Generate Premiere Pro XML timeline.

**Parameters:**
- `data` (dict) - Timeline data (clips, markers, settings)
- `output_path` (str) - Path to save `.xml` file

**Returns:** `str` - Path to generated file

### `export_davinci_edl(data, output_path)`

Generate DaVinci Resolve EDL.

**Parameters:**
- `data` (dict) - Timeline data (clips, markers, settings)
- `output_path` (str) - Path to save `.edl` file

**Returns:** `str` - Path to generated file

### `export_davinci_xml(data, output_path)`

Generate DaVinci Resolve XML.

**Parameters:**
- `data` (dict) - Timeline data (clips, markers, settings)
- `output_path` (str) - Path to save `.xml` file

**Returns:** `str` - Path to generated file

## References

- [FCPXML Reference](https://developer.apple.com/documentation/professional_video_applications/fcpxml_reference)
- [CMX 3600 EDL Specification](http://xmil.biz/EDL-X/CMX3600.pdf)
- [Premiere Pro Import/Export](https://helpx.adobe.com/premiere-pro/using/supported-file-formats.html)
- [DaVinci Resolve Manual](https://www.blackmagicdesign.com/products/davinciresolve)

## License

MIT License - Carolina Elite Events

## Author

Built by Jarvis for Video Culler 🎬
