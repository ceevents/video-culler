import { useStore } from '../store'

export default function AnalysisView() {
  const { analysisProgress } = useStore()

  if (!analysisProgress) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="text-center">
          <div className="mb-4 h-12 w-12 animate-spin rounded-full border-4 border-purple-500 border-t-transparent"></div>
          <p className="text-gray-400">Initializing analysis...</p>
        </div>
      </div>
    )
  }

  const progress = analysisProgress.total > 0 
    ? (analysisProgress.current / analysisProgress.total) * 100 
    : 0

  return (
    <div className="flex h-full items-center justify-center">
      <div className="w-full max-w-2xl px-8">
        <div className="mb-6 text-center">
          <h2 className="mb-2 text-2xl font-bold">Analyzing Videos</h2>
          <p className="text-gray-400">
            {analysisProgress.message || 'Processing your footage...'}
          </p>
        </div>

        {/* Progress Bar */}
        <div className="mb-4 overflow-hidden rounded-full bg-gray-800">
          <div
            className="h-3 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-300"
            style={{ width: `${progress}%` }}
          ></div>
        </div>

        {/* Progress Text */}
        <div className="flex justify-between text-sm text-gray-500">
          <span>
            {analysisProgress.current} of {analysisProgress.total} videos
          </span>
          <span>{Math.round(progress)}%</span>
        </div>

        {/* Current File */}
        {analysisProgress.currentFile && (
          <div className="mt-6 rounded-lg border border-gray-800 bg-gray-800/50 p-4">
            <p className="text-sm text-gray-500">Currently analyzing:</p>
            <p className="font-mono text-sm text-purple-400">{analysisProgress.currentFile}</p>
          </div>
        )}

        {/* Info Box */}
        <div className="mt-8 rounded-lg border border-blue-900 bg-blue-900/20 p-4">
          <p className="text-sm text-blue-300">
            💡 We're extracting frames and calculating focus scores for each video. This may take a
            few minutes depending on the number and length of your clips.
          </p>
        </div>
      </div>
    </div>
  )
}
