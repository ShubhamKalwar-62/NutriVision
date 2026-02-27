import { useState, useCallback } from 'react'
import { Helmet } from 'react-helmet-async'
import { motion, AnimatePresence } from 'framer-motion'
import axios from 'axios'
import ImageDropzone from '../components/ImageDropzone'
import ResultsPanel from '../components/ResultsPanel'
import { useAuth } from '../context/AuthContext'
import { HiOutlineSparkles, HiOutlineRefresh } from 'react-icons/hi'
import './AnalyzePage.css'

export default function AnalyzePage() {
  const { authHeader } = useAuth()
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleFileSelect = useCallback((f) => {
    setFile(f)
    setPreview(URL.createObjectURL(f))
    setResult(null)
    setError(null)
  }, [])

  const handleAnalyze = async () => {
    if (!file) return
    setLoading(true)
    setError(null)
    setResult(null)

    const form = new FormData()
    form.append('image', file)

    try {
      const { data } = await axios.post('/api/analyze', form, {
        headers: { 'Content-Type': 'multipart/form-data', ...authHeader() },
        timeout: 120000,
      })
      setResult(data)
    } catch (err) {
      const msg = err.response?.data?.error || err.message || 'Something went wrong'
      setError(msg)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setFile(null)
    setPreview(null)
    setResult(null)
    setError(null)
  }

  return (
    <>
      <Helmet>
        <title>Analyze Food — NutriVision</title>
        <meta
          name="description"
          content="Upload your food image to get instant AI-powered calorie, mass, and volume estimates using YOLOv4 deep learning."
        />
      </Helmet>

      <section className="analyze">
        <div className="analyze__inner">
          {/* Header */}
          <motion.div
            className="analyze__header"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <h1 className="analyze__title">
              <HiOutlineSparkles className="analyze__title-icon" />
              Analyze Your Food
            </h1>
            <p className="analyze__subtitle">
              Upload a food image with your thumb visible for size calibration, then hit analyze.
            </p>
          </motion.div>

          {/* Upload area */}
          <motion.div
            className="analyze__upload"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <ImageDropzone onFileSelect={handleFileSelect} preview={preview} disabled={loading} />
          </motion.div>

          {/* Actions */}
          <motion.div
            className="analyze__actions"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            {file && !loading && (
              <>
                <button className="btn btn--primary btn--lg" onClick={handleAnalyze}>
                  <HiOutlineSparkles size={18} />
                  Analyze Image
                </button>
                <button className="btn btn--ghost" onClick={handleReset}>
                  <HiOutlineRefresh size={16} />
                  Reset
                </button>
              </>
            )}
          </motion.div>

          {/* Loading */}
          <AnimatePresence>
            {loading && (
              <motion.div
                className="analyze__loading"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
              >
                <div className="analyze__spinner" />
                <p className="analyze__loading-text">Analyzing your food…</p>
                <p className="analyze__loading-hint">
                  Running YOLOv4 detection → Segmentation → Volume & Calorie estimation
                </p>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Error */}
          <AnimatePresence>
            {error && (
              <motion.div
                className="analyze__error"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
              >
                <p><strong>Error:</strong> {error}</p>
                <p className="analyze__error-hint">
                  Make sure the API server is running on port 5000. Run: <code>python api_server.py</code>
                </p>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Results */}
          <AnimatePresence>
            {result && (
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.5 }}
              >
                <ResultsPanel data={result} />
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </section>
    </>
  )
}
