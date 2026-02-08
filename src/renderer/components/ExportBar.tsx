import { useState } from 'react'
import { useStore } from '../store'

export default function ExportBar() {
  const { clips, selectedDuration } = useStore()
  const [isExporting, setIsExporting] = useState(false)

  const selectedClips = clips.filter((c) => c.selected)
  const selectedCount = selectedClips.length

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const handleExport = async () => {
    if (selectedCount === 0) {
      alert('Please select at least one clip to export.')
      return
    }

    setIsExporting(true)

    try {
      const result = await window.api.exportTimeline(selectedClips, {
        projectName: 'Wedding Timeline',
        format: 'fcpxml'
      })

      if (result.success) {
        alert(`Timeline exported successfully to:\n${result.path}`)
      } else {
        alert(`Export failed: ${result.message}`)
      }
    } catch (error) {
      console.error('Export error:', error)
      alert('An error occurred during export.')
    } finally {
      setIsExporting(false)
    }
  }

  const selectAllHighScoring = () => {
    // Auto-select clips with score >= 70
    clips.forEach((clip) => {
      if (clip.focusScore >= 70 && !clip.selected) {
        useStore.getState().toggleClipSelection(clip.id)
      }
    })
  }

  const clearSelection = () => {
    clips.forEach((clip) => {
      if (clip.selected) {
        useStore.getState().toggleClipSelection(clip.id)
      }
    })
  }

  return (
    <div className="border-t border-gray-800 bg-gray-950 px-6 py-4">
      <div className="flex items-center justify-between">
        {/* Stats */}
        <div className="flex items-center gap-6">
          <div>
            <span className="text-sm text-gray-500">Selected:</span>
            <span className="ml-2 font-semibold text-purple-400">
              {selectedCount} clips
            </span>
          </div>
          
          <div>
            <span className="text-sm text-gray-500">Duration:</span>
            <span className="ml-2 font-semibold text-purple-400">
              {formatTime(selectedDuration())}
            </span>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-3">
          <button
            onClick={selectAllHighScoring}
            className="rounded bg-gray-800 px-4 py-2 text-sm font-medium transition-colors hover:bg-gray-700"
          >
            Select High Scores (≥70)
          </button>
          
          <button
            onClick={clearSelection}
            disabled={selectedCount === 0}
            className="rounded bg-gray-800 px-4 py-2 text-sm font-medium transition-colors hover:bg-gray-700 disabled:opacity-50"
          >
            Clear Selection
          </button>
          
          <button
            onClick={handleExport}
            disabled={selectedCount === 0 || isExporting}
            className="rounded-lg bg-gradient-to-r from-purple-500 to-pink-500 px-6 py-2 font-semibold transition-all hover:from-purple-600 hover:to-pink-600 disabled:opacity-50"
          >
            {isExporting ? 'Exporting...' : 'Export Timeline'}
          </button>
        </div>
      </div>
    </div>
  )
}
