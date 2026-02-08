import { VideoClip } from '../../shared/types'
import { useStore } from '../store'

interface ClipCardProps {
  clip: VideoClip
}

export default function ClipCard({ clip }: ClipCardProps) {
  const { toggleClipSelection } = useStore()

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-400'
    if (score >= 60) return 'text-yellow-400'
    if (score >= 40) return 'text-orange-400'
    return 'text-red-400'
  }

  const getScoreBg = (score: number) => {
    if (score >= 80) return 'bg-green-500/20 border-green-500/50'
    if (score >= 60) return 'bg-yellow-500/20 border-yellow-500/50'
    if (score >= 40) return 'bg-orange-500/20 border-orange-500/50'
    return 'bg-red-500/20 border-red-500/50'
  }

  return (
    <div
      className={`group relative overflow-hidden rounded-lg border transition-all ${
        clip.selected
          ? 'border-purple-500 bg-purple-900/20 ring-2 ring-purple-500/50'
          : 'border-gray-800 bg-gray-800/50 hover:border-gray-700'
      }`}
    >
      {/* Selection Checkbox */}
      <div className="absolute right-2 top-2 z-10">
        <input
          type="checkbox"
          checked={clip.selected}
          onChange={() => toggleClipSelection(clip.id)}
          className="h-5 w-5 cursor-pointer rounded border-gray-600 bg-gray-900 text-purple-500 focus:ring-2 focus:ring-purple-500"
        />
      </div>

      {/* Thumbnail */}
      <div className="relative aspect-video w-full overflow-hidden bg-gray-900">
        {clip.thumbnail ? (
          <img
            src={clip.thumbnail}
            alt={clip.filename}
            className="h-full w-full object-cover"
          />
        ) : (
          <div className="flex h-full items-center justify-center">
            <svg
              className="h-12 w-12 text-gray-700"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"
              />
            </svg>
          </div>
        )}

        {/* Score Badge */}
        <div className={`absolute bottom-2 left-2 rounded border px-2 py-1 ${getScoreBg(clip.focusScore)}`}>
          <span className={`text-xs font-bold ${getScoreColor(clip.focusScore)}`}>
            {clip.focusScore} / 100
          </span>
        </div>

        {/* Duration */}
        <div className="absolute bottom-2 right-2 rounded bg-black/80 px-2 py-1">
          <span className="text-xs text-white">{formatDuration(clip.duration)}</span>
        </div>
      </div>

      {/* Info */}
      <div className="p-3">
        <h3 className="mb-1 truncate text-sm font-medium" title={clip.filename}>
          {clip.filename}
        </h3>
        
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span className="truncate">{clip.directory}</span>
          <span className="ml-2 whitespace-nowrap">
            {clip.width}x{clip.height}
          </span>
        </div>
      </div>
    </div>
  )
}
