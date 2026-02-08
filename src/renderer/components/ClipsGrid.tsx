import { useState } from 'react'
import { useStore } from '../store'
import ClipCard from './ClipCard'

export default function ClipsGrid() {
  const { clips } = useStore()
  const [sortBy, setSortBy] = useState<'score' | 'name' | 'duration'>('score')
  const [filterDirectory, setFilterDirectory] = useState<string>('all')

  // Get unique directories
  const directories = Array.from(new Set(clips.map((c) => c.directory)))

  // Filter and sort clips
  const filteredClips = clips.filter((clip) =>
    filterDirectory === 'all' ? true : clip.directory === filterDirectory
  )

  const sortedClips = [...filteredClips].sort((a, b) => {
    switch (sortBy) {
      case 'score':
        return b.overallScore - a.overallScore
      case 'name':
        return a.filename.localeCompare(b.filename)
      case 'duration':
        return b.duration - a.duration
      default:
        return 0
    }
  })

  return (
    <div className="flex h-full flex-col">
      {/* Toolbar */}
      <div className="flex items-center justify-between border-b border-gray-800 bg-gray-900 px-6 py-4">
        <div className="flex items-center gap-4">
          <div>
            <label className="mr-2 text-sm text-gray-400">Filter:</label>
            <select
              value={filterDirectory}
              onChange={(e) => setFilterDirectory(e.target.value)}
              className="rounded bg-gray-800 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="all">All Folders</option>
              {directories.map((dir) => (
                <option key={dir} value={dir}>
                  {dir}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="mr-2 text-sm text-gray-400">Sort by:</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="rounded bg-gray-800 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="score">Focus Score</option>
              <option value="name">Name</option>
              <option value="duration">Duration</option>
            </select>
          </div>
        </div>

        <div className="text-sm text-gray-400">
          <span className="text-white">{clips.length}</span> clips found
        </div>
      </div>

      {/* Grid */}
      <div className="flex-1 overflow-y-auto p-6">
        {sortedClips.length === 0 ? (
          <div className="flex h-full items-center justify-center">
            <p className="text-gray-500">No clips found in this folder.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {sortedClips.map((clip) => (
              <ClipCard key={clip.id} clip={clip} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
