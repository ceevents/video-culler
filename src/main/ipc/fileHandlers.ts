import { ipcMain, dialog } from 'electron'
import { readdir } from 'fs/promises'
import { join, basename, dirname, relative } from 'path'
import { IPC_CHANNELS, VideoFile } from '../../shared/types'
import ffmpeg from 'fluent-ffmpeg'
import ffmpegInstaller from '@ffmpeg-installer/ffmpeg'

ffmpeg.setFfmpegPath(ffmpegInstaller.path)

const VIDEO_EXTENSIONS = ['.mp4', '.mov', '.avi', '.mxf', '.m4v', '.mkv']

export function setupFileHandlers() {
  // Select folder dialog
  ipcMain.handle(IPC_CHANNELS.SELECT_FOLDER, async () => {
    const result = await dialog.showOpenDialog({
      properties: ['openDirectory'],
      title: 'Select Video Project Folder'
    })

    if (result.canceled) {
      return null
    }

    return result.filePaths[0]
  })

  // Scan videos in selected folder
  ipcMain.handle(IPC_CHANNELS.SCAN_VIDEOS, async (_, folderPath: string) => {
    const videoFiles: VideoFile[] = []

    async function scanDirectory(dirPath: string) {
      const entries = await readdir(dirPath, { withFileTypes: true })

      for (const entry of entries) {
        const fullPath = join(dirPath, entry.name)

        if (entry.isDirectory()) {
          await scanDirectory(fullPath)
        } else if (entry.isFile()) {
          const ext = entry.name.toLowerCase().substring(entry.name.lastIndexOf('.'))
          if (VIDEO_EXTENSIONS.includes(ext)) {
            try {
              const metadata = await getVideoMetadata(fullPath)
              const relativePath = relative(folderPath, dirname(fullPath))
              
              videoFiles.push({
                id: fullPath,
                path: fullPath,
                filename: basename(fullPath),
                directory: relativePath || 'root',
                ...metadata
              })
            } catch (error) {
              console.error(`Failed to read metadata for ${fullPath}:`, error)
            }
          }
        }
      }
    }

    await scanDirectory(folderPath)
    return videoFiles
  })
}

function getVideoMetadata(filePath: string): Promise<{
  duration: number
  width: number
  height: number
  fps: number
  codec: string
}> {
  return new Promise((resolve, reject) => {
    ffmpeg.ffprobe(filePath, (err, metadata) => {
      if (err) {
        reject(err)
        return
      }

      const videoStream = metadata.streams.find((s) => s.codec_type === 'video')
      if (!videoStream) {
        reject(new Error('No video stream found'))
        return
      }

      // Parse frame rate (e.g., "30/1" -> 30)
      let fps = 30
      if (videoStream.r_frame_rate) {
        const parts = videoStream.r_frame_rate.split('/')
        if (parts.length === 2) {
          fps = parseInt(parts[0]) / parseInt(parts[1])
        }
      }

      resolve({
        duration: metadata.format.duration || 0,
        width: videoStream.width || 0,
        height: videoStream.height || 0,
        fps,
        codec: videoStream.codec_name || 'unknown'
      })
    })
  })
}
