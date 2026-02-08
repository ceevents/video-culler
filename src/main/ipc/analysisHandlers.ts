import { ipcMain, BrowserWindow } from 'electron'
import { IPC_CHANNELS, VideoFile, VideoClip, AnalysisProgress } from '../../shared/types'
import ffmpeg from 'fluent-ffmpeg'
import sharp from 'sharp'
import { mkdtemp, writeFile, readFile } from 'fs/promises'
import { join } from 'path'
import { tmpdir } from 'os'
import { setClips, getClips } from './clipHandlers'

export function setupAnalysisHandlers() {
  ipcMain.handle(IPC_CHANNELS.ANALYZE_VIDEOS, async (event, videoFiles: VideoFile[]) => {
    const analyzedClips: VideoClip[] = []
    const total = videoFiles.length

    for (let i = 0; i < videoFiles.length; i++) {
      const video = videoFiles[i]
      
      // Send progress update
      sendProgress(event.sender, {
        stage: 'analyzing',
        current: i + 1,
        total,
        currentFile: video.filename,
        message: `Analyzing ${video.filename}...`
      })

      try {
        const clip = await analyzeVideo(video)
        analyzedClips.push(clip)
      } catch (error) {
        console.error(`Failed to analyze ${video.filename}:`, error)
        // Continue with next video
      }
    }

    sendProgress(event.sender, {
      stage: 'complete',
      current: total,
      total,
      message: 'Analysis complete!'
    })

    setClips(analyzedClips)
    return analyzedClips
  })

  ipcMain.handle(IPC_CHANNELS.GET_CLIPS, () => {
    return getClips()
  })
}

async function analyzeVideo(video: VideoFile): Promise<VideoClip> {
  // Create temp directory for frames
  const tempDir = await mkdtemp(join(tmpdir(), 'video-culler-'))
  
  // Extract frames at 1 second intervals
  const frames = await extractFrames(video.path, tempDir, 1)
  
  // Calculate focus scores for each frame
  const focusScores = await Promise.all(frames.map((frame) => calculateFocusScore(frame)))
  
  // Calculate average focus score
  const avgFocusScore = focusScores.reduce((sum, score) => sum + score, 0) / focusScores.length
  
  // Generate thumbnail from middle frame
  const middleFrameIndex = Math.floor(frames.length / 2)
  const thumbnail = await generateThumbnail(frames[middleFrameIndex])
  
  // For MVP, overall score is just focus score
  const overallScore = Math.round(avgFocusScore)
  
  return {
    ...video,
    focusScore: overallScore,
    overallScore,
    selected: false,
    inPoint: 0,
    outPoint: video.duration,
    thumbnail
  }
}

function extractFrames(videoPath: string, outputDir: string, interval: number): Promise<string[]> {
  return new Promise((resolve, reject) => {
    const frames: string[] = []
    let frameCount = 0

    ffmpeg(videoPath)
      .outputOptions([
        `-vf fps=1/${interval}` // Extract one frame every N seconds
      ])
      .output(join(outputDir, 'frame-%04d.png'))
      .on('end', async () => {
        // List all generated frames
        const { readdir } = await import('fs/promises')
        const files = await readdir(outputDir)
        const framePaths = files
          .filter((f) => f.startsWith('frame-'))
          .sort()
          .map((f) => join(outputDir, f))
        resolve(framePaths)
      })
      .on('error', reject)
      .run()
  })
}

async function calculateFocusScore(imagePath: string): Promise<number> {
  // Read image and convert to grayscale
  const image = await sharp(imagePath).grayscale().raw().toBuffer({ resolveWithObject: true })

  const { data, info } = image
  const { width, height } = info

  // Calculate Laplacian variance
  // This measures edge sharpness - higher values = more in focus
  let variance = 0
  const laplacian: number[] = []

  // Apply Laplacian kernel (simplified 3x3)
  for (let y = 1; y < height - 1; y++) {
    for (let x = 1; x < width - 1; x++) {
      const idx = y * width + x

      const center = data[idx]
      const top = data[(y - 1) * width + x]
      const bottom = data[(y + 1) * width + x]
      const left = data[y * width + (x - 1)]
      const right = data[y * width + (x + 1)]

      // Laplacian: -4*center + top + bottom + left + right
      const lap = Math.abs(-4 * center + top + bottom + left + right)
      laplacian.push(lap)
    }
  }

  // Calculate variance
  const mean = laplacian.reduce((sum, val) => sum + val, 0) / laplacian.length
  variance = laplacian.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / laplacian.length

  // Normalize to 0-100 scale (adjust multiplier based on testing)
  const score = Math.min(100, (variance / 100) * 100)
  return score
}

async function generateThumbnail(imagePath: string): Promise<string> {
  const buffer = await sharp(imagePath).resize(320, 180, { fit: 'cover' }).jpeg().toBuffer()

  return `data:image/jpeg;base64,${buffer.toString('base64')}`
}

function sendProgress(sender: Electron.WebContents, progress: AnalysisProgress) {
  sender.send(IPC_CHANNELS.ANALYSIS_PROGRESS, progress)
}
