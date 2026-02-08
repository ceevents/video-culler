import { useState } from 'react'
import { useStore } from '../store'

export default function WelcomeScreen() {
  const { setSelectedFolder, setClips, setIsAnalyzing } = useStore()
  const [isLoading, setIsLoading] = useState(false)

  const handleSelectFolder = async () => {
    setIsLoading(true)
    
    try {
      // Open folder selection dialog
      const folderPath = await window.api.selectFolder()
      
      if (!folderPath) {
        setIsLoading(false)
        return
      }
      
      setSelectedFolder(folderPath)
      
      // Scan for videos
      const videoFiles = await window.api.scanVideos(folderPath)
      
      if (videoFiles.length === 0) {
        alert('No video files found in the selected folder.')
        setIsLoading(false)
        return
      }
      
      // Start analysis
      setIsAnalyzing(true)
      const analyzedClips = await window.api.analyzeVideos(videoFiles)
      setClips(analyzedClips)
      setIsAnalyzing(false)
    } catch (error) {
      console.error('Error:', error)
      alert('An error occurred while processing videos.')
      setIsLoading(false)
      setIsAnalyzing(false)
    }
  }

  return (
    <div className="flex h-full items-center justify-center">
      <div className="max-w-2xl text-center">
        <div className="mb-8 inline-block rounded-2xl bg-gradient-to-br from-purple-500 to-pink-500 p-6">
          <svg
            className="h-16 w-16 text-white"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z"
            />
          </svg>
        </div>
        
        <h2 className="mb-4 text-4xl font-bold">Welcome to Video Culler</h2>
        
        <p className="mb-8 text-lg text-gray-400">
          AI-powered video culling for wedding videographers. Select a folder containing your
          wedding footage, and let's find the best clips.
        </p>
        
        <div className="mb-8 rounded-lg border border-gray-800 bg-gray-800/50 p-6 text-left">
          <h3 className="mb-3 font-semibold text-gray-300">Expected folder structure:</h3>
          <pre className="text-sm text-gray-400">
{`Wedding_Project/
├── A-Roll/        # Primary footage
├── B-Roll/        # Detail shots
└── RAW/           # Camera cards`}
          </pre>
        </div>
        
        <button
          onClick={handleSelectFolder}
          disabled={isLoading}
          className="rounded-lg bg-gradient-to-r from-purple-500 to-pink-500 px-8 py-4 text-lg font-semibold transition-all hover:from-purple-600 hover:to-pink-600 disabled:opacity-50"
        >
          {isLoading ? 'Loading...' : 'Select Project Folder'}
        </button>
      </div>
    </div>
  )
}
