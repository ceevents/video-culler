# Development Guide

## Project Structure

```
video-culler/
├── src/
│   ├── main/               # Electron main process
│   │   ├── index.ts       # Main entry point
│   │   └── ipc/           # IPC handlers
│   │       ├── index.ts           # Handler registry
│   │       ├── fileHandlers.ts    # File system operations
│   │       ├── analysisHandlers.ts # Video analysis
│   │       ├── clipHandlers.ts    # Clip state management
│   │       └── exportHandlers.ts  # FCPXML export
│   │
│   ├── preload/           # Electron preload scripts
│   │   ├── index.ts       # API bridge to renderer
│   │   └── index.d.ts     # Type definitions
│   │
│   ├── renderer/          # React UI
│   │   ├── components/    # React components
│   │   │   ├── WelcomeScreen.tsx
│   │   │   ├── AnalysisView.tsx
│   │   │   ├── ClipsGrid.tsx
│   │   │   ├── ClipCard.tsx
│   │   │   └── ExportBar.tsx
│   │   ├── App.tsx        # Main app component
│   │   ├── store.ts       # Zustand state management
│   │   ├── main.tsx       # React entry point
│   │   ├── index.css      # Tailwind CSS
│   │   └── index.html     # HTML template
│   │
│   └── shared/            # Shared code
│       └── types.ts       # TypeScript types
│
├── resources/             # App resources
│   └── icon.png          # App icon
│
├── out/                   # Build output (gitignored)
├── node_modules/          # Dependencies (gitignored)
└── package.json
```

## Development Workflow

### 1. Start Development Server

```bash
npm run dev
```

This starts:
- Electron main process in watch mode
- Vite dev server for renderer
- Hot reload for both processes

### 2. Make Changes

The app will automatically reload when you save changes to:
- **Main process** (`src/main/`) - Electron restarts
- **Renderer** (`src/renderer/`) - Hot module replacement (HMR)

### 3. Build for Production

```bash
npm run build        # Build without packaging
npm run build:mac    # Build + create macOS .dmg
npm run build:win    # Build + create Windows installer
```

## Key Technologies

### Electron
- **Main Process** - Node.js environment with full system access
- **Renderer Process** - Chromium browser with React UI
- **Preload Scripts** - Bridge between main and renderer (contextBridge)

### Video Processing
- **FFmpeg** - Frame extraction, video metadata
- **Sharp** - Image processing, thumbnail generation
- **Laplacian Variance** - Focus detection algorithm

### State Management
- **Zustand** - Lightweight React state management
- Clips stored in main process, synced to renderer via IPC

### Styling
- **Tailwind CSS** - Utility-first CSS framework
- Custom gradient theme (purple to pink)

## IPC Communication

### Flow
```
Renderer (UI)  →  Preload (Bridge)  →  Main (Backend)
      ↑                                      ↓
      └──────────────────────────────────────┘
```

### Example: Analyzing Videos

**Renderer:**
```typescript
const clips = await window.api.analyzeVideos(videoFiles)
```

**Preload:**
```typescript
analyzeVideos: (videoFiles) => 
  ipcRenderer.invoke(IPC_CHANNELS.ANALYZE_VIDEOS, videoFiles)
```

**Main:**
```typescript
ipcMain.handle(IPC_CHANNELS.ANALYZE_VIDEOS, async (event, videoFiles) => {
  // Process videos...
  return analyzedClips
})
```

## Focus Detection Algorithm

### Laplacian Variance Method

1. **Extract Frame** - FFmpeg extracts PNG at 1-second interval
2. **Grayscale Conversion** - Sharp converts to grayscale
3. **Laplacian Kernel** - Apply edge detection:
   ```
   [ 0  1  0 ]
   [ 1 -4  1 ]
   [ 0  1  0 ]
   ```
4. **Calculate Variance** - Higher variance = sharper edges = better focus
5. **Normalize** - Scale to 0-100 score

### Code
```typescript
// Simplified version
const laplacian = []
for (let y = 1; y < height - 1; y++) {
  for (let x = 1; x < width - 1; x++) {
    const center = data[y * width + x]
    const top = data[(y - 1) * width + x]
    const bottom = data[(y + 1) * width + x]
    const left = data[y * width + (x - 1)]
    const right = data[y * width + (x + 1)]
    
    const lap = Math.abs(-4 * center + top + bottom + left + right)
    laplacian.push(lap)
  }
}

const mean = sum(laplacian) / laplacian.length
const variance = sum(laplacian.map(v => (v - mean) ** 2)) / laplacian.length
const score = Math.min(100, (variance / 100) * 100)
```

## FCPXML Export

### Structure
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.10">
  <resources>
    <!-- Video files -->
    <asset id="r1" src="file:///path/to/video.mov"/>
  </resources>
  <library>
    <event name="Video Culler Import">
      <project name="Timeline">
        <sequence>
          <spine>
            <!-- Timeline clips -->
            <asset-clip ref="r1" offset="0s" start="2s" duration="5s"/>
          </spine>
        </sequence>
      </project>
    </event>
  </library>
</fcpxml>
```

### Import to Final Cut Pro
1. Open Final Cut Pro
2. File → Import → XML
3. Select exported `.fcpxml` file
4. Timeline appears in Libraries panel

## Testing

### Manual Testing Checklist

- [ ] Import folder with videos
- [ ] Progress bar shows during analysis
- [ ] Clips appear in grid with thumbnails
- [ ] Focus scores display correctly (0-100)
- [ ] Can filter by directory
- [ ] Can sort by score/name/duration
- [ ] Can select/deselect clips
- [ ] Selected clip count updates
- [ ] Duration calculation correct
- [ ] Export generates valid FCPXML
- [ ] FCPXML imports to Final Cut Pro

### Test Videos
Create a test folder:
```
Test_Project/
├── A-Roll/
│   ├── sharp_clip.mp4      # High score expected
│   └── blurry_clip.mp4     # Low score expected
└── B-Roll/
    └── medium_clip.mp4     # Mid score expected
```

## Common Issues

### Build Errors

**Error: Cannot find module 'sharp'**
- Solution: Run `npm install` again (sharp has native bindings)

**Error: FFmpeg not found**
- Solution: The app bundles FFmpeg via `@ffmpeg-installer/ffmpeg`
- Check `ffmpeg.setFfmpegPath()` in fileHandlers.ts

### Runtime Errors

**Video not loading**
- Check codec support (H.264/H.265 work best)
- Verify file path encoding (no special characters)

**Analysis stuck**
- Check temp directory permissions
- Verify FFmpeg can write frames to `/tmp`

**Export fails**
- Check write permissions for output path
- Verify selected clips have valid paths

## Performance

### Optimization Tips

1. **Frame Extraction** - Currently 1 frame/second
   - Reduce to 1 frame/2s for faster analysis
   - Trade-off: less accurate focus scores

2. **Parallel Processing** - Process multiple videos concurrently
   - Currently sequential (one at a time)
   - Add worker threads for analysis

3. **Thumbnail Caching** - Cache thumbnails to disk
   - Currently generates on each analysis
   - Store in `~/.video-culler/cache/`

4. **Smart Sampling** - Only analyze first 30 seconds of long clips
   - Full analysis can be slow for 1-hour clips
   - Assume first 30s representative of whole clip

## Future Enhancements

### Phase 2 Features
- [ ] Audio analysis (speech, music, applause)
- [ ] Face detection (prioritize clips with faces)
- [ ] Motion detection (flag shaky clips)
- [ ] Scene categorization (CLIP model)
- [ ] Auto-select best clips

### Phase 3 Features
- [ ] Premiere Pro XML export
- [ ] DaVinci Resolve export
- [ ] Batch processing (multiple projects)
- [ ] Cloud processing option
- [ ] Team collaboration

## Resources

- [Electron Docs](https://www.electronjs.org/docs)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [FCPXML Reference](https://developer.apple.com/documentation/professional_video_applications/fcpxml_reference)
- [Sharp API](https://sharp.pixelplumbing.com/)
- [Laplacian Operator](https://en.wikipedia.org/wiki/Laplace_operator)

---

**Last Updated:** 2026-02-08  
**Author:** Jarvis / Carolina Elite Events
