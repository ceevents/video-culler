# Quick Start Guide

Get Video Culler running in 5 minutes! 🚀

## Prerequisites

- **Node.js** 18+ (check: `node --version`)
- **npm** 9+ (check: `npm --version`)
- **macOS** or **Windows** (Linux untested)

## Installation

```bash
# Clone or navigate to project
cd ~/Projects/video-culler

# Install dependencies
npm install

# Start development server
npm run dev
```

The app window should open automatically!

## First Run

### 1. Prepare Test Footage

Create a test folder with some wedding video clips:

```
Test_Wedding/
├── A-Roll/
│   ├── ceremony_001.mp4
│   └── ceremony_002.mp4
└── B-Roll/
    └── details_001.mp4
```

**Tip:** Use short clips (10-30 seconds) for faster testing.

### 2. Import Folder

1. Click **"Select Project Folder"**
2. Choose your `Test_Wedding` folder
3. Wait for analysis (progress bar shows status)

### 3. Review Clips

- Clips appear in a grid
- Each shows:
  - **Thumbnail** preview
  - **Focus Score** (0-100, color-coded)
  - **Duration** and resolution
  - **Directory** (A-Roll, B-Roll, etc.)

### 4. Select Clips

- Click the **checkbox** on clips to include
- Or use **"Select High Scores (≥70)"** button
- Watch the selected duration update at bottom

### 5. Export Timeline

1. Click **"Export Timeline"** at bottom-right
2. Choose save location
3. Name your file (e.g., `wedding_timeline.fcpxml`)
4. Click **Save**

### 6. Open in Final Cut Pro

1. Open **Final Cut Pro X**
2. Go to **File → Import → XML...**
3. Select your exported `.fcpxml` file
4. The timeline appears in your library! 🎉

## Understanding Focus Scores

| Score | Color | Meaning |
|-------|-------|---------|
| 80-100 | 🟢 Green | Sharp, in focus - great clip! |
| 60-79 | 🟡 Yellow | Acceptable focus - usable |
| 40-59 | 🟠 Orange | Soft focus - review manually |
| 0-39 | 🔴 Red | Out of focus - probably skip |

**How it works:** The app extracts frames from each video and calculates edge sharpness using the Laplacian variance algorithm. Sharper edges = higher score = better focus.

## Tips & Tricks

### Faster Analysis
- Use shorter clips during testing
- Limit number of videos (< 50 for quick tests)
- Analysis speed: ~10-20 videos/minute (depends on length)

### Better Results
- Ensure good lighting in footage
- Stable camera helps (less motion blur)
- Higher resolution videos (1080p+) score better
- H.264 codec recommended (MOV, MP4)

### Workflow
1. **Import raw footage** from all cameras
2. **Review scores** - flag clips < 40 as potential rejects
3. **Quick select** high-scoring clips (≥70)
4. **Manual review** - watch 60-70 range clips
5. **Export** selected clips to timeline
6. **Edit in FCP** - trim, color grade, add music

## Keyboard Shortcuts

_(Coming soon - not yet implemented)_

- `Space` - Play/pause preview
- `I` - Set in point
- `O` - Set out point
- `A` - Select all
- `Cmd+E` - Export timeline

## Troubleshooting

### "No video files found"
- Check folder contains `.mp4`, `.mov`, or `.avi` files
- Ensure files aren't in hidden folders

### "Analysis stuck at 0%"
- Check temp folder permissions
- Verify FFmpeg can write to `/tmp`
- Try restarting the app

### "Export failed"
- Ensure you have write permission to save location
- Check disk space (FCPXML files are small, but still)
- Try a different save location

### Videos won't play in Final Cut Pro
- Exported XML just references original files
- Don't move/rename original videos after export
- Ensure FCP can access the video file paths

## Sample Project

Want to test without your own footage?

1. Download free stock wedding videos:
   - [Pexels - Wedding](https://www.pexels.com/search/videos/wedding/)
   - [Pixabay - Wedding](https://pixabay.com/videos/search/wedding/)

2. Organize into folders:
   ```
   Sample_Project/
   ├── Ceremony/
   └── Reception/
   ```

3. Import and test!

## Next Steps

- Read [DEVELOPMENT.md](./DEVELOPMENT.md) for technical details
- Check [README.md](./README.md) for feature roadmap
- Review [PLAN.md](~/.openclaw/workspace/projects/video-culler/PLAN.md) for full vision

## Support

Questions? Issues?

- Create an issue on GitHub
- Check the development logs: `out/` folder
- Run with DevTools: `View → Toggle Developer Tools` in app

---

**Happy culling! 🎬✨**
