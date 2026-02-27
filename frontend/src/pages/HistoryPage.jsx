import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Helmet } from 'react-helmet-async'
import { motion, AnimatePresence } from 'framer-motion'
import axios from 'axios'
import {
  HiOutlineClock,
  HiOutlineFire,
  HiOutlineTrash,
  HiOutlineEye,
  HiOutlinePhotograph,
  HiOutlineArrowRight,
} from 'react-icons/hi'
import { useAuth } from '../context/AuthContext'
import './HistoryPage.css'

const FOOD_EMOJI = {
  Apple: '🍎', Banana: '🍌', Carrot: '🥕', Onion: '🧅',
  Orange: '🍊', Qiwi: '🥝', Tomato: '🍅',
}

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { type: 'spring', stiffness: 120, damping: 18 } },
}

export default function HistoryPage() {
  const { authHeader, isAuthenticated } = useAuth()
  const navigate = useNavigate()
  const [scans, setScans] = useState([])
  const [loading, setLoading] = useState(true)
  const [expandedId, setExpandedId] = useState(null)
  const [detail, setDetail] = useState(null)
  const [detailLoading, setDetailLoading] = useState(false)

  useEffect(() => {
    if (!isAuthenticated) return
    axios
      .get('/api/history', { headers: authHeader() })
      .then(({ data }) => setScans(data.history))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [isAuthenticated, authHeader])

  const handleDelete = async (scanId) => {
    try {
      await axios.delete(`/api/history/${scanId}`, { headers: authHeader() })
      setScans((prev) => prev.filter((s) => s.id !== scanId))
      if (expandedId === scanId) {
        setExpandedId(null)
        setDetail(null)
      }
    } catch {
      /* silently fail */
    }
  }

  const handleExpand = async (scanId) => {
    if (expandedId === scanId) {
      setExpandedId(null)
      setDetail(null)
      return
    }
    setExpandedId(scanId)
    setDetailLoading(true)
    try {
      const { data } = await axios.get(`/api/history/${scanId}`, { headers: authHeader() })
      setDetail(data)
    } catch {
      setDetail(null)
    } finally {
      setDetailLoading(false)
    }
  }

  if (!isAuthenticated) {
    return (
      <>
        <Helmet><title>History — NutriVision</title></Helmet>
        <section className="history-page">
          <div className="history-empty">
            <HiOutlinePhotograph size={48} className="history-empty__icon" />
            <h2>Sign in to view your scan history</h2>
            <Link to="/login" className="btn btn--primary">Sign In</Link>
          </div>
        </section>
      </>
    )
  }

  return (
    <>
      <Helmet>
        <title>Scan History — NutriVision</title>
        <meta name="description" content="View your past food calorie scans and results." />
      </Helmet>

      <section className="history-page">
        <div className="history-page__inner">
          <motion.div
            className="history-page__header"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h1 className="history-page__title">
              <HiOutlineClock className="history-page__title-icon" />
              Scan History
            </h1>
            <p className="history-page__subtitle">
              All your past food analyses are stored here. Click any scan to see the detailed result.
            </p>
          </motion.div>

          {loading ? (
            <div className="history-loading">
              <div className="analyze__spinner" />
              <p>Loading history…</p>
            </div>
          ) : scans.length === 0 ? (
            <motion.div className="history-empty" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <HiOutlinePhotograph size={48} className="history-empty__icon" />
              <h2>No scans yet</h2>
              <p>Upload and analyze your first food image to get started.</p>
              <Link to="/analyze" className="btn btn--primary">
                Analyze Now <HiOutlineArrowRight size={16} />
              </Link>
            </motion.div>
          ) : (
            <motion.div className="history-list" initial="hidden" animate="visible" variants={{ visible: { transition: { staggerChildren: 0.06 } } }}>
              {scans.map((scan) => {
                const foods = scan.detections.filter((d) => d.label !== 'thumb')
                const isOpen = expandedId === scan.id

                return (
                  <motion.div key={scan.id} className={`history-card ${isOpen ? 'history-card--open' : ''}`} variants={fadeUp}>
                    <div className="history-card__row" onClick={() => handleExpand(scan.id)}>
                      <div className="history-card__emojis">
                        {foods.slice(0, 5).map((d, i) => (
                          <span key={i}>{FOOD_EMOJI[d.label] || '🍽️'}</span>
                        ))}
                      </div>
                      <div className="history-card__info">
                        <h3 className="history-card__filename">{scan.filename || 'Untitled scan'}</h3>
                        <span className="history-card__date">
                          {new Date(scan.scanned_at).toLocaleString()}
                        </span>
                      </div>
                      <div className="history-card__stats">
                        <span className="history-card__cal">
                          <HiOutlineFire size={16} />
                          {Math.round(scan.total_calories)} kcal
                        </span>
                        <span className="history-card__count">{foods.length} food{foods.length !== 1 ? 's' : ''}</span>
                      </div>
                      <div className="history-card__actions">
                        <button className="history-card__btn history-card__btn--view" title="Toggle details">
                          <HiOutlineEye size={18} />
                        </button>
                        <button
                          className="history-card__btn history-card__btn--delete"
                          title="Delete scan"
                          onClick={(e) => { e.stopPropagation(); handleDelete(scan.id) }}
                        >
                          <HiOutlineTrash size={18} />
                        </button>
                      </div>
                    </div>

                    {/* Expanded detail */}
                    <AnimatePresence>
                      {isOpen && (
                        <motion.div
                          className="history-detail"
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: 'auto', opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          transition={{ duration: 0.3 }}
                        >
                          {detailLoading ? (
                            <div className="history-detail__loading">
                              <div className="analyze__spinner" />
                            </div>
                          ) : detail ? (
                            <div className="history-detail__content">
                              {detail.result_image && (
                                <img
                                  src={`data:image/jpeg;base64,${detail.result_image}`}
                                  alt="Scan result"
                                  className="history-detail__image"
                                />
                              )}
                              <div className="history-detail__foods">
                                {detail.detections
                                  .filter((d) => d.label !== 'thumb')
                                  .map((d, i) => (
                                    <div key={i} className="history-detail__food">
                                      <span className="history-detail__emoji">{FOOD_EMOJI[d.label] || '🍽️'}</span>
                                      <span className="history-detail__label">{d.label}</span>
                                      <span className="history-detail__conf">{d.confidence}%</span>
                                      {d.calories_kcal != null && (
                                        <span className="history-detail__kcal">{Math.round(d.calories_kcal)} kcal</span>
                                      )}
                                      {d.mass_g != null && (
                                        <span className="history-detail__mass">{d.mass_g}g</span>
                                      )}
                                    </div>
                                  ))}
                              </div>
                              <div className="history-detail__meta">
                                <span>Detection: {detail.detection_time}s</span>
                                <span>Thumb: {detail.thumb_found ? '✅' : '⚠️ Not found'}</span>
                              </div>
                            </div>
                          ) : (
                            <p className="history-detail__error">Could not load details.</p>
                          )}
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </motion.div>
                )
              })}
            </motion.div>
          )}
        </div>
      </section>
    </>
  )
}
