import { ipcMain, dialog } from 'electron'
import { writeFile } from 'fs/promises'
import { IPC_CHANNELS, VideoClip, ExportOptions } from '../../shared/types'

export function setupExportHandlers() {
  ipcMain.handle(IPC_CHANNELS.EXPORT_TIMELINE, async (_, clips: VideoClip[], options: Partial<ExportOptions>) => {
    // Show save dialog
    const result = await dialog.showSaveDialog({
      title: 'Export Timeline',
      defaultPath: `${options.projectName || 'timeline'}.fcpxml`,
      filters: [{ name: 'Final Cut Pro XML', extensions: ['fcpxml'] }]
    })

    if (result.canceled || !result.filePath) {
      return { success: false, message: 'Export cancelled' }
    }

    try {
      const xml = generateFCPXML(clips, options.projectName || 'Video Culler Timeline')
      await writeFile(result.filePath, xml, 'utf-8')
      return { success: true, path: result.filePath }
    } catch (error) {
      console.error('Export failed:', error)
      return { success: false, message: error instanceof Error ? error.message : 'Export failed' }
    }
  })
}

function generateFCPXML(clips: VideoClip[], projectName: string): string {
  const selectedClips = clips.filter((c) => c.selected)

  // Generate resources (unique video files)
  const uniqueFiles = Array.from(new Set(selectedClips.map((c) => c.path)))
  const resources = uniqueFiles.map((path, index) => {
    const clip = selectedClips.find((c) => c.path === path)!
    return `    <asset id="r${index + 1}" src="file://${encodeURI(path)}" start="0s" duration="${clip.duration}s" hasVideo="1" format="r0" hasAudio="1"/>`
  }).join('\n')

  // Generate timeline clips
  let currentOffset = 0
  const timelineClips = selectedClips.map((clip) => {
    const resourceId = uniqueFiles.indexOf(clip.path) + 1
    const duration = clip.outPoint - clip.inPoint
    const start = clip.inPoint
    
    const clipXml = `      <asset-clip ref="r${resourceId}" offset="${currentOffset}s" name="${clip.filename}" start="${start}s" duration="${duration}s">
        <note>Focus Score: ${clip.focusScore}</note>
      </asset-clip>`
    
    currentOffset += duration
    return clipXml
  }).join('\n')

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.10">
  <resources>
    <format id="r0" name="FFVideoFormat1080p30" frameDuration="100/3000s" width="1920" height="1080" colorSpace="1-1-1 (Rec. 709)"/>
${resources}
  </resources>
  <library>
    <event name="Video Culler Import">
      <project name="${projectName}">
        <sequence format="r0" tcStart="0s" tcFormat="NDF" duration="${currentOffset}s">
          <spine>
${timelineClips}
          </spine>
        </sequence>
      </project>
    </event>
  </library>
</fcpxml>`

  return xml
}
