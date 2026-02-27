import { motion } from 'framer-motion'
import {
  HiOutlineLightningBolt,
  HiOutlineCube,
  HiOutlineScale,
  HiOutlineFire,
  HiOutlineClock,
  HiOutlineExclamationCircle,
} from 'react-icons/hi'
import './ResultsPanel.css'

const FOOD_EMOJI = {
  Apple: '🍎',
  Banana: '🍌',
  Carrot: '🥕',
  Onion: '🧅',
  Orange: '🍊',
  Qiwi: '🥝',
  Tomato: '🍅',
  thumb: '👍',
}

const containerVariants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.1 } },
}

const cardVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { type: 'spring', stiffness: 120, damping: 18 } },
}

export default function ResultsPanel({ data }) {
  if (!data) return null

  const { detections, detection_time, result_image, thumb_found } = data
  const foods = detections.filter((d) => d.label !== 'thumb')
  const totalCalories = foods.reduce((s, d) => s + (d.calories_kcal || 0), 0)

  return (
    <motion.section
      className="results"
      initial="hidden"
      animate="visible"
      variants={containerVariants}
      aria-label="Analysis results"
    >
      {/* Summary strip */}
      <motion.div className="results__summary" variants={cardVariants}>
        <div className="results__stat">
          <HiOutlineClock className="results__stat-icon" />
          <span className="results__stat-value">{detection_time}s</span>
          <span className="results__stat-label">Detection</span>
        </div>
        <div className="results__stat">
          <HiOutlineLightningBolt className="results__stat-icon" />
          <span className="results__stat-value">{foods.length}</span>
          <span className="results__stat-label">Foods Found</span>
        </div>
        <div className="results__stat results__stat--highlight">
          <HiOutlineFire className="results__stat-icon" />
          <span className="results__stat-value">{Math.round(totalCalories)}</span>
          <span className="results__stat-label">Total kcal</span>
        </div>
        <div className="results__stat">
          <span className="results__stat-icon">{thumb_found ? '✅' : '⚠️'}</span>
          <span className="results__stat-value">{thumb_found ? 'Yes' : 'No'}</span>
          <span className="results__stat-label">Thumb Ref</span>
        </div>
      </motion.div>

      {!thumb_found && (
        <motion.div className="results__warning" variants={cardVariants}>
          <HiOutlineExclamationCircle size={20} />
          <p>No thumb detected — calorie estimation requires a visible thumb for size calibration. Only detection results are shown.</p>
        </motion.div>
      )}

      {/* Annotated image */}
      {result_image && (
        <motion.div className="results__image-wrap" variants={cardVariants}>
          <h3 className="results__section-title">Annotated Result</h3>
          <img
            src={`data:image/jpeg;base64,${result_image}`}
            alt="Annotated food detection result"
            className="results__image"
          />
        </motion.div>
      )}

      {/* Food cards */}
      {foods.length > 0 && (
        <div>
          <h3 className="results__section-title">Detected Foods</h3>
          <div className="results__grid">
            {foods.map((d, i) => (
              <motion.article key={i} className="food-card" variants={cardVariants}>
                <div className="food-card__header">
                  <span className="food-card__emoji">{FOOD_EMOJI[d.label] || '🍽️'}</span>
                  <div>
                    <h4 className="food-card__name">{d.label}</h4>
                    <span className="food-card__conf">{d.confidence}% confidence</span>
                  </div>
                </div>

                {d.calories_kcal != null ? (
                  <div className="food-card__metrics">
                    <div className="food-card__metric">
                      <HiOutlineFire className="food-card__metric-icon food-card__metric-icon--cal" />
                      <span className="food-card__metric-value">{d.calories_kcal}</span>
                      <span className="food-card__metric-label">kcal</span>
                    </div>
                    <div className="food-card__metric">
                      <HiOutlineScale className="food-card__metric-icon" />
                      <span className="food-card__metric-value">{d.mass_g}</span>
                      <span className="food-card__metric-label">grams</span>
                    </div>
                    <div className="food-card__metric">
                      <HiOutlineCube className="food-card__metric-icon" />
                      <span className="food-card__metric-value">{d.volume_cm3}</span>
                      <span className="food-card__metric-label">cm³</span>
                    </div>
                  </div>
                ) : (
                  <p className="food-card__no-cal">
                    Calorie data unavailable (thumb not detected)
                  </p>
                )}

                {/* Calorie bar */}
                {d.calories_kcal != null && (
                  <div className="food-card__bar-wrap">
                    <motion.div
                      className="food-card__bar"
                      initial={{ width: 0 }}
                      animate={{ width: `${Math.min((d.calories_kcal / Math.max(totalCalories, 1)) * 100, 100)}%` }}
                      transition={{ duration: 0.8, ease: 'easeOut' }}
                    />
                  </div>
                )}
              </motion.article>
            ))}
          </div>
        </div>
      )}
    </motion.section>
  )
}
