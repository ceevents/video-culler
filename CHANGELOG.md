# Changelog

All notable changes to Video Culler will be documented in this file.

## [0.1.0] - 2026-02-08

### ✨ Initial MVP Release

#### Features
- **Video Import** - Select folder containing wedding footage
- **Automatic Scanning** - Recursively find all video files (MP4, MOV, AVI, MXF, M4V, MKV)
- **Focus Detection** - Laplacian variance algorithm scores each clip (0-100)
- **Grid UI** - Visual grid of all clips with thumbnails
- **Clip Selection** - Manual checkbox selection for timeline
- **FCPXML Export** - Generate Final Cut Pro X timeline
- **Progress Tracking** - Live progress bar during analysis
- **Filtering** - Filter clips by directory (A-Roll, B-Roll, etc.)
- **Sorting** - Sort by focus score, name, or duration
- **Duration Calculator** - Real-time selected clip duration
- **Auto-Select** - Quick select all high-scoring clips (≥70)

#### Technical
- Electron 28 + React 18 + TypeScript
- Vite for fast builds and HMR
- Tailwind CSS for styling
- FFmpeg for video processing
- Sharp for image analysis
- Zustand for state management

#### Documentation
- README.md - Overview and features
- QUICKSTART.md - 5-minute getting started guide
- DEVELOPMENT.md - Full technical documentation
- PLAN.md - Product vision and roadmap

### 🐛 Bug Fixes
- Fixed build error with HTML import path
- Replaced unsafe eval() with proper frame rate parsing

### 📝 Notes
- Focus detection currently analyzes 1 frame per second
- Export only supports FCPXML (Premiere/Resolve coming soon)
- No audio analysis yet (coming in v0.2)
- No face detection yet (coming in v0.2)

---

## Upcoming

### [0.2.0] - Planned
- Audio analysis (speech, music, applause detection)
- Face detection (prioritize clips with people)
- Motion detection (flag shaky clips)
- Scene categorization (CLIP AI model)
- Auto-select algorithm (weighted scoring)
- Premiere Pro XML export

### [0.3.0] - Planned
- DaVinci Resolve export
- Batch processing (multiple projects)
- Settings panel (thresholds, intervals)
- Clip preview player
- In/Out point trimming

### [1.0.0] - Planned
- Cloud processing option
- Team collaboration
- Project management
- Custom templates
- Plugin system

---

**Legend:**
- ✨ New feature
- 🐛 Bug fix
- 🔧 Improvement
- 📝 Documentation
- ⚠️ Breaking change
