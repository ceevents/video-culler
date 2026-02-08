import { create } from 'zustand'
import { VideoClip, AnalysisProgress } from '../shared/types'

interface AppState {
  clips: VideoClip[]
  selectedFolder: string | null
  isAnalyzing: boolean
  analysisProgress: AnalysisProgress | null
  
  setClips: (clips: VideoClip[]) => void
  setSelectedFolder: (folder: string | null) => void
  setIsAnalyzing: (analyzing: boolean) => void
  setAnalysisProgress: (progress: AnalysisProgress | null) => void
  toggleClipSelection: (clipId: string) => void
  
  // Computed values
  selectedClips: () => VideoClip[]
  totalDuration: () => number
  selectedDuration: () => number
}

export const useStore = create<AppState>((set, get) => ({
  clips: [],
  selectedFolder: null,
  isAnalyzing: false,
  analysisProgress: null,
  
  setClips: (clips) => set({ clips }),
  setSelectedFolder: (folder) => set({ selectedFolder: folder }),
  setIsAnalyzing: (analyzing) => set({ isAnalyzing: analyzing }),
  setAnalysisProgress: (progress) => set({ analysisProgress: progress }),
  
  toggleClipSelection: (clipId) => {
    const clips = get().clips
    const updatedClips = clips.map((clip) =>
      clip.id === clipId ? { ...clip, selected: !clip.selected } : clip
    )
    set({ clips: updatedClips })
    
    // Sync with main process
    window.api.toggleSelection(clipId)
  },
  
  selectedClips: () => get().clips.filter((c) => c.selected),
  
  totalDuration: () => get().clips.reduce((sum, clip) => sum + clip.duration, 0),
  
  selectedDuration: () =>
    get().clips
      .filter((c) => c.selected)
      .reduce((sum, clip) => sum + (clip.outPoint - clip.inPoint), 0)
}))
