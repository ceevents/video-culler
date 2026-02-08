import { setupFileHandlers } from './fileHandlers'
import { setupAnalysisHandlers } from './analysisHandlers'
import { setupClipHandlers } from './clipHandlers'
import { setupExportHandlers } from './exportHandlers'

export function setupIpcHandlers() {
  setupFileHandlers()
  setupAnalysisHandlers()
  setupClipHandlers()
  setupExportHandlers()
}
