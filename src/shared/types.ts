// Shared types between main and renderer processes

export interface VideoFile {
  id: string
  path: string
  filename: string
  directory: string // A-Roll, B-Roll, RAW, etc.
  duration: number // seconds
  width: number
  height: number
  fps: number
  codec: string
  thumbnail?: string // base64 or path
}

export interface VideoClip extends VideoFile {
  focusScore: number // 0-100
  compositionScore?: number // 0-100
  audioScore?: number // 0-100
  overallScore: number // weighted average
  selected: boolean
  inPoint: number // seconds
  outPoint: number // seconds
  category?: string // Ceremony, Reception, etc.
}

export interface AnalysisProgress {
  stage: 'scanning' | 'extracting' | 'analyzing' | 'complete' | 'error'
  current: number
  total: number
  currentFile?: string
  message?: string
}

export interface ProjectMetadata {
  name: string
  path: string
  createdAt: number
  totalClips: number
  selectedClips: number
  targetDuration: number // seconds
}

export interface ExportOptions {
  format: 'fcpxml' | 'premiere' | 'resolve'
  outputPath: string
  projectName: string
  includeAudio: boolean
}

// IPC Channel names
export const IPC_CHANNELS = {
  // File operations
  SELECT_FOLDER: 'file:select-folder',
  SCAN_VIDEOS: 'file:scan-videos',
  
  // Analysis
  ANALYZE_VIDEOS: 'analysis:analyze-videos',
  ANALYSIS_PROGRESS: 'analysis:progress',
  
  // Clips
  GET_CLIPS: 'clips:get-all',
  UPDATE_CLIP: 'clips:update',
  TOGGLE_SELECTION: 'clips:toggle-selection',
  
  // Export
  EXPORT_TIMELINE: 'export:timeline',
  
  // Settings
  GET_SETTINGS: 'settings:get',
  UPDATE_SETTINGS: 'settings:update'
} as const
