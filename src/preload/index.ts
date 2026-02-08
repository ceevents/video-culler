import { contextBridge, ipcRenderer } from 'electron'
import { IPC_CHANNELS, VideoFile, VideoClip, ExportOptions, AnalysisProgress } from '../shared/types'

// Expose protected methods that allow the renderer process to use ipcRenderer
const api = {
  selectFolder: () => ipcRenderer.invoke(IPC_CHANNELS.SELECT_FOLDER),
  
  scanVideos: (folderPath: string) => ipcRenderer.invoke(IPC_CHANNELS.SCAN_VIDEOS, folderPath),
  
  analyzeVideos: (videoFiles: VideoFile[]) => ipcRenderer.invoke(IPC_CHANNELS.ANALYZE_VIDEOS, videoFiles),
  
  onAnalysisProgress: (callback: (progress: AnalysisProgress) => void) => {
    const subscription = (_: any, progress: AnalysisProgress) => callback(progress)
    ipcRenderer.on(IPC_CHANNELS.ANALYSIS_PROGRESS, subscription)
    return () => ipcRenderer.removeListener(IPC_CHANNELS.ANALYSIS_PROGRESS, subscription)
  },
  
  getClips: () => ipcRenderer.invoke(IPC_CHANNELS.GET_CLIPS),
  
  toggleSelection: (clipId: string) => ipcRenderer.invoke(IPC_CHANNELS.TOGGLE_SELECTION, clipId),
  
  updateClip: (clip: Partial<VideoClip>) => ipcRenderer.invoke(IPC_CHANNELS.UPDATE_CLIP, clip),
  
  exportTimeline: (clips: VideoClip[], options: Partial<ExportOptions>) => 
    ipcRenderer.invoke(IPC_CHANNELS.EXPORT_TIMELINE, clips, options)
}

contextBridge.exposeInMainWorld('api', api)

export type API = typeof api
