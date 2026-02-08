# Video Culler

AI-powered video culling tool for wedding videographers. Automatically analyzes wedding footage, detects focus quality, and helps you select the best clips for your highlight reel.

## Features

- 🎥 **Smart Video Analysis** - Automatically scans folders of video files
- 🎯 **Focus Detection** - Uses Laplacian variance to calculate focus scores (0-100)
- 📊 **Visual Grid** - Browse all clips with thumbnails and scores
- ✅ **Manual Selection** - Click to select/deselect clips for your timeline
- 📤 **FCPXML Export** - Generate timeline for Final Cut Pro X

## Tech Stack

- **Electron** - Desktop app framework
- **React** - UI framework
- **Tailwind CSS** - Styling
- **TypeScript** - Type safety
- **Vite** - Build tool
- **FFmpeg** - Video processing
- **Sharp** - Image analysis
- **Zustand** - State management

## Installation

```bash
cd ~/Projects/video-culler
npm install
```

## Development

```bash
npm run dev
```

## Build

```bash
# Build for macOS
npm run build:mac

# Build for Windows
npm run build:win
```

## Usage

1. **Import Folder** - Select a folder containing your wedding videos
   - Recommended structure: `A-Roll/`, `B-Roll/`, `RAW/`
   
2. **Wait for Analysis** - The app will:
   - Scan all video files (MP4, MOV, etc.)
   - Extract frames at 1-second intervals
   - Calculate focus scores using Laplacian variance
   - Generate thumbnails

3. **Review & Select**
   - Browse clips in a grid view
   - Filter by folder (A-Roll, B-Roll, etc.)
   - Sort by score, name, or duration
   - Check clips to include in timeline
   - Use "Select High Scores" for quick selection

4. **Export Timeline**
   - Click "Export Timeline"
   - Save FCPXML file
   - Open in Final Cut Pro X

## Focus Scoring

The focus score (0-100) measures image sharpness using **Laplacian variance**:

- **80-100** (Green) - Sharp, in focus
- **60-79** (Yellow) - Acceptable focus
- **40-59** (Orange) - Soft focus
- **0-39** (Red) - Out of focus

## Roadmap

### MVP (Current)
- ✅ Video folder import
- ✅ Focus detection
- ✅ Grid UI with thumbnails
- ✅ Manual selection
- ✅ FCPXML export

### Future Features
- [ ] Audio analysis (speech, music, applause detection)
- [ ] Scene categorization (ceremony, reception, etc.)
- [ ] Composition scoring (face detection, rule of thirds)
- [ ] Auto-select best clips based on scoring
- [ ] Premiere Pro XML export
- [ ] DaVinci Resolve export
- [ ] Batch processing multiple projects

## License

MIT License - Carolina Elite Events

## Author

Built by Jarvis for wedding videographers 🎬
