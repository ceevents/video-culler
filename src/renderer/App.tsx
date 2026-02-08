import { useEffect, useState } from 'react'
import { useStore } from './store'
import WelcomeScreen from './components/WelcomeScreen'
import AnalysisView from './components/AnalysisView'
import ClipsGrid from './components/ClipsGrid'
import ExportBar from './components/ExportBar'

function App() {
  const { clips, selectedFolder, isAnalyzing, setAnalysisProgress } = useStore()
  const [view, setView] = useState<'welcome' | 'analyzing' | 'clips'>('welcome')

  useEffect(() => {
    // Listen for analysis progress
    const unsubscribe = window.api.onAnalysisProgress((progress) => {
      setAnalysisProgress(progress)
      
      if (progress.stage === 'complete') {
        setView('clips')
      }
    })

    return () => {
      unsubscribe()
    }
  }, [])

  useEffect(() => {
    if (isAnalyzing) {
      setView('analyzing')
    }
  }, [isAnalyzing])

  useEffect(() => {
    if (clips.length > 0 && !isAnalyzing) {
      setView('clips')
    }
  }, [clips, isAnalyzing])

  return (
    <div className="flex h-screen flex-col bg-gray-900 text-white">
      {/* Header */}
      <header className="flex items-center justify-between border-b border-gray-800 bg-gray-950 px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500"></div>
          <h1 className="text-xl font-bold">Video Culler</h1>
        </div>
        
        {selectedFolder && (
          <div className="text-sm text-gray-400">
            <span className="text-gray-500">Project:</span> {selectedFolder.split('/').pop()}
          </div>
        )}
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-hidden">
        {view === 'welcome' && <WelcomeScreen />}
        {view === 'analyzing' && <AnalysisView />}
        {view === 'clips' && <ClipsGrid />}
      </main>

      {/* Export Bar (only show when clips are loaded) */}
      {view === 'clips' && clips.length > 0 && <ExportBar />}
    </div>
  )
}

export default App
