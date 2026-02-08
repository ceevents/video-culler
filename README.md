# Video Culler

AI-powered desktop app for wedding videographers to automatically cull footage and generate edit-ready timelines for Final Cut Pro and Premiere Pro.

## Features

- **Smart Analysis**: Automatically scores clips based on focus, composition, and audio
- **Scene Detection**: Categorizes footage by wedding event (ceremony, reception, speeches, etc.)
- **Auto-Selection**: Picks the best clips to hit your target highlight duration
- **Timeline Export**: Generates FCPXML for Final Cut Pro or XML for Premiere Pro

## Architecture

```
video-culler/
├── desktop/          # Electron + React UI
├── engine/           # Python analysis backend
│   ├── analysis/     # Focus, composition, audio scoring
│   ├── export/       # FCPXML, Premiere XML generation
│   └── selection/    # Smart clip selection algorithm
└── shared/           # Shared types and schemas
```

## Tech Stack

**Desktop App:**
- Electron 28+
- React 18 + Vite
- Tailwind CSS
- Zustand (state management)

**Analysis Engine:**
- Python 3.11+
- FastAPI + Uvicorn
- OpenCV (focus detection)
- face_recognition (composition)
- librosa (audio analysis)
- FFmpeg (video processing)

## Getting Started

### Prerequisites
- Node.js 20+
- Python 3.11+
- FFmpeg installed and in PATH

### Installation

```bash
# Clone the repo
git clone https://github.com/Carolina-Elite-Events/video-culler.git
cd video-culler

# Install desktop app
cd desktop
npm install

# Install Python engine
cd ../engine
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Run the app
cd ../desktop
npm run dev
```

## Workflow

1. **Import** - Select folder containing wedding video files
2. **Analyze** - App extracts frames and scores each clip
3. **Review** - Browse clips in grid, preview and adjust selections
4. **Export** - Generate timeline for your NLE of choice

## Expected File Structure

```
Wedding_Project/
├── A-Roll/          # Primary ceremony/reception footage
├── B-Roll/          # Detail shots, decor, candids
├── Audio/           # External audio recordings
└── RAW/             # Original camera cards
```

## License

Proprietary - Carolina Elite Events

---

*Built for wedding videographers who want to spend less time culling and more time creating.*
