import { ipcMain } from 'electron'
import { IPC_CHANNELS, VideoClip } from '../../shared/types'

// This would ideally be in a state manager, but for MVP we'll use module-level storage
// Import from analysisHandlers to share state
let clips: VideoClip[] = []

export function setupClipHandlers() {
  ipcMain.handle(IPC_CHANNELS.TOGGLE_SELECTION, async (_, clipId: string) => {
    const clip = clips.find((c) => c.id === clipId)
    if (clip) {
      clip.selected = !clip.selected
    }
    return clips
  })

  ipcMain.handle(IPC_CHANNELS.UPDATE_CLIP, async (_, updatedClip: Partial<VideoClip>) => {
    const clipIndex = clips.findIndex((c) => c.id === updatedClip.id)
    if (clipIndex !== -1) {
      clips[clipIndex] = { ...clips[clipIndex], ...updatedClip }
    }
    return clips
  })
}

// Export function to allow other modules to access clips
export function getClips() {
  return clips
}

export function setClips(newClips: VideoClip[]) {
  clips = newClips
}
