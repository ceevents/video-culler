# Export Format Version Compatibility

This document tracks tested compatibility with different NLE versions.

## Final Cut Pro X

### FCPXML 1.10 Format

**Tested & Working:**
- ✅ Final Cut Pro X 10.8 (2024)
- ✅ Final Cut Pro X 10.7
- ✅ Final Cut Pro X 10.6

**Should Work (untested):**
- ⚠️ Final Cut Pro X 10.4+

**Known Issues:**
- Older versions (pre-10.4) may not support FCPXML 1.10
- Some metadata keys may not be recognized in older versions
- Marker colors may differ slightly between versions

**Import Path:**
1. File → Import → XML
2. Select `.fcpxml` file
3. Timeline appears in current event

**Media Relinking:**
- FCP X uses absolute file paths
- If media moves, you'll need to relink
- Right-click → Relink Files

---

## Adobe Premiere Pro

### Premiere Pro XML (xmeml v5)

**Tested & Working:**
- ✅ Premiere Pro CC 2024
- ✅ Premiere Pro CC 2023

**Should Work (untested):**
- ⚠️ Premiere Pro CC 2020+
- ⚠️ Premiere Pro CC 2019

**Known Issues:**
- Based on Final Cut Pro 7 XML interchange format
- Some Premiere-specific effects won't be preserved
- Audio tracks are included but empty (video only currently)
- Frame rate must match project settings for smooth import

**Import Path:**
1. File → Import
2. Select `.xml` file
3. Sequence appears in Project panel
4. Double-click to open in timeline

**Media Relinking:**
- Premiere uses `pathurl` file:// references
- Media Browser: Right-click → Link Media
- Can relink to different folder if structure matches

**Recommended Settings:**
- Create a Premiere project with matching:
  - Frame rate (23.976, 24, 29.97, 30, 60)
  - Resolution (1080p, 4K)
  - Timebase matching framerate

---

## DaVinci Resolve

### EDL Format (CMX 3600)

**Tested & Working:**
- ✅ DaVinci Resolve 19 (2024)
- ✅ DaVinci Resolve 18

**Should Work:**
- ⚠️ DaVinci Resolve 17+
- ⚠️ DaVinci Resolve 16 (Studio)

**Known Issues:**
- EDL format is limited (no effects, basic metadata only)
- Reel names truncated to 8 characters
- Markers appear as comments (not native markers)
- Source file paths in comments for reference

**Import Path:**
1. File → Import → Timeline → Import AAF, EDL, XML...
2. Select `.edl` file
3. Set frame rate if prompted
4. Timeline is created with clips
5. Relink media if needed

**Recommended:**
- EDL is the most reliable format for DaVinci
- Simple and widely compatible
- Use XML if you need more metadata

### XML Format (xmeml v4)

**Tested & Working:**
- ✅ DaVinci Resolve 19
- ✅ DaVinci Resolve 18

**Should Work:**
- ⚠️ DaVinci Resolve 17+

**Known Issues:**
- Based on FCP 7 XML (older format)
- Some advanced features may not import
- Prefer EDL for simplicity

**Import Path:**
1. File → Import → Timeline → Import AAF, EDL, XML...
2. Select `.xml` file
3. Timeline is created

---

## Frame Rate Compatibility

### Drop-Frame vs Non-Drop-Frame

| Frame Rate | Timecode Format | NLE Support |
|------------|-----------------|-------------|
| 23.976     | DF (;)          | FCP, Premiere, Resolve |
| 24         | NDF (:)         | FCP, Premiere, Resolve |
| 25         | NDF (:)         | FCP, Premiere, Resolve |
| 29.97      | DF (;)          | FCP, Premiere, Resolve |
| 30         | NDF (:)         | FCP, Premiere, Resolve |
| 50         | NDF (:)         | FCP, Premiere, Resolve |
| 59.94      | DF (;)          | FCP, Premiere, Resolve |
| 60         | NDF (:)         | FCP, Premiere, Resolve |

**Notes:**
- DF (drop-frame) uses `;` separator in timecode: `00:00:00;00`
- NDF (non-drop-frame) uses `:` separator: `00:00:00:00`
- NTSC rates (23.976, 29.97, 59.94) typically use drop-frame
- Film/PAL rates use non-drop-frame

---

## Resolution Support

All formats support:
- ✅ SD (720x480, 720x576)
- ✅ HD (1280x720, 1920x1080)
- ✅ 2K (2048x1080)
- ✅ UHD/4K (3840x2160)
- ✅ DCI 4K (4096x2160)
- ✅ Custom resolutions

---

## Testing Checklist

When testing with a new NLE version:

### FCPXML
- [ ] Imports without errors
- [ ] All clips appear on timeline
- [ ] In/out points are correct
- [ ] Markers appear with correct names
- [ ] Marker colors are preserved
- [ ] Metadata is readable (score, category)
- [ ] File paths resolve correctly
- [ ] Timecode matches expected values

### Premiere XML
- [ ] Imports without errors
- [ ] All clips appear in sequence
- [ ] In/out points are correct
- [ ] Markers appear on clips
- [ ] Clip labels show categories
- [ ] File paths resolve correctly
- [ ] Timecode/frame rate is correct
- [ ] Audio tracks are present

### DaVinci EDL
- [ ] EDL imports successfully
- [ ] Correct number of events
- [ ] Timecode values are accurate
- [ ] Comments contain metadata
- [ ] File paths are in comments
- [ ] Frame rate matches
- [ ] Can relink to source files

### DaVinci XML
- [ ] XML imports successfully
- [ ] All clips on timeline
- [ ] Markers are present
- [ ] Frame rate is correct
- [ ] Resolution is correct

---

## Reporting Issues

If you encounter compatibility issues:

1. **Document the NLE version:**
   - Application name and version number
   - Build number if available
   - Operating system

2. **Describe the problem:**
   - What's not working?
   - Error messages?
   - Missing features?

3. **Attach sample files:**
   - Generated export file
   - Screenshot of error or issue
   - Log files if available

4. **Test with minimal data:**
   - Try exporting just 1-2 clips
   - Remove markers and metadata
   - Simplify to isolate the issue

---

## Future Compatibility

### Planned Testing
- [ ] Avid Media Composer (via AAF)
- [ ] Adobe After Effects (for motion graphics prep)
- [ ] Vegas Pro
- [ ] HitFilm Pro

### Format Extensions
- [ ] AAF (Advanced Authoring Format)
- [ ] OMF (Open Media Framework) 
- [ ] MXF (Material Exchange Format)
- [ ] ProRes RAW metadata

---

## Last Updated

2024-02-08 - Initial version compatibility testing
