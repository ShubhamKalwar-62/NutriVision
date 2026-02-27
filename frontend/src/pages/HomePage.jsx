import { Link } from 'react-router-dom'
import { Helmet } from 'react-helmet-async'
import { motion } from 'framer-motion'
import {
  HiOutlineLightningBolt,
  HiOutlineEye,
  HiOutlineChartBar,
  HiOutlineShieldCheck,
  HiOutlineArrowRight,
} from 'react-icons/hi'
import './HomePage.css'

const fadeUp = {
  hidden: { opacity: 0, y: 40 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.12, duration: 0.6, ease: [0.22, 1, 0.36, 1] },
  }),
}

const supportedFoods = [
  { emoji: '🍎', name: 'Apple', cal: '52 kcal/100g' },
  { emoji: '🍌', name: 'Banana', cal: '89 kcal/100g' },
  { emoji: '🥕', name: 'Carrot', cal: '41 kcal/100g' },
  { emoji: '🧅', name: 'Onion', cal: '40 kcal/100g' },
  { emoji: '🍊', name: 'Orange', cal: '47 kcal/100g' },
  { emoji: '🥝', name: 'Kiwi', cal: '44 kcal/100g' },
  { emoji: '🍅', name: 'Tomato', cal: '18 kcal/100g' },
]

const features = [
  {
    icon: <HiOutlineEye size={28} />,
    title: 'YOLOv4 Detection',
    desc: 'Real‑time object detection with custom‑trained YOLOv4 achieving 98.6% accuracy on food items.',
  },
  {
    icon: <HiOutlineChartBar size={28} />,
    title: 'Volume & Mass Estimation',
    desc: 'Uses thumb reference for pixel‑to‑cm calibration, computing 3D volume from 2D contours.',
  },
  {
    icon: <HiOutlineLightningBolt size={28} />,
    title: 'Instant Calorie Results',
    desc: 'Get per‑item calorie breakdown in seconds—no manual measuring or guessing required.',
  },
  {
    icon: <HiOutlineShieldCheck size={28} />,
    title: 'Privacy First',
    desc: 'All processing happens on your machine. No images are stored or sent to third‑party servers.',
  },
]

const steps = [
  { num: '01', title: 'Upload Image', desc: 'Take a photo of your food with your thumb visible for scale reference.' },
  { num: '02', title: 'AI Analysis', desc: 'Our YOLOv4 model detects each food item and segments it for measurement.' },
  { num: '03', title: 'Get Results', desc: 'View detected foods with calorie, mass, and volume estimates instantly.' },
]

export default function HomePage() {
  return (
    <>
      <Helmet>
        <title>NutriVision — AI‑Powered Food Calorie Estimation</title>
        <meta
          name="description"
          content="Upload a food photo and get instant AI‑powered calorie estimates. Powered by YOLOv4 deep learning with 98.6% accuracy."
        />
      </Helmet>

      {/* ── Hero ───────────────────────────────── */}
      <section className="hero">
        <div className="hero__bg">
          <div className="hero__orb hero__orb--1" />
          <div className="hero__orb hero__orb--2" />
          <div className="hero__grid-overlay" />
        </div>

        <div className="hero__content">
          <motion.div className="hero__badge" variants={fadeUp} initial="hidden" animate="visible" custom={0}>
            <HiOutlineLightningBolt size={14} />
            <span>Powered by YOLOv4 Deep Learning</span>
          </motion.div>

          <motion.h1 className="hero__title" variants={fadeUp} initial="hidden" animate="visible" custom={1}>
            Know Your Calories.
            <br />
            <span className="hero__title-accent">Instantly.</span>
          </motion.h1>

          <motion.p className="hero__subtitle" variants={fadeUp} initial="hidden" animate="visible" custom={2}>
            Upload a photo of your food and let our AI estimate calories, mass, and volume
            using computer vision and deep learning — all in seconds.
          </motion.p>

          <motion.div className="hero__actions" variants={fadeUp} initial="hidden" animate="visible" custom={3}>
            <Link to="/analyze" className="btn btn--primary btn--lg">
              Analyze My Food
              <HiOutlineArrowRight size={18} />
            </Link>
            <Link to="/about" className="btn btn--ghost btn--lg">
              Learn More
            </Link>
          </motion.div>

          <motion.div className="hero__stats" variants={fadeUp} initial="hidden" animate="visible" custom={4}>
            <div className="hero__stat">
              <span className="hero__stat-value">98.6%</span>
              <span className="hero__stat-label">Detection Accuracy</span>
            </div>
            <div className="hero__stat-divider" />
            <div className="hero__stat">
              <span className="hero__stat-value">7</span>
              <span className="hero__stat-label">Food Categories</span>
            </div>
            <div className="hero__stat-divider" />
            <div className="hero__stat">
              <span className="hero__stat-value">&lt;2s</span>
              <span className="hero__stat-label">Processing Time</span>
            </div>
          </motion.div>
        </div>
      </section>

      {/* ── Supported Foods ────────────────────── */}
      <section className="section foods-section" aria-label="Supported foods">
        <div className="section__inner">
          <motion.h2 className="section__title" variants={fadeUp} initial="hidden" whileInView="visible" viewport={{ once: true }}>
            Supported Foods
          </motion.h2>
          <motion.p className="section__desc" variants={fadeUp} initial="hidden" whileInView="visible" viewport={{ once: true }} custom={1}>
            Our custom‑trained model recognizes these food categories with high accuracy.
          </motion.p>

          <div className="foods-grid">
            {supportedFoods.map((food, i) => (
              <motion.div
                key={food.name}
                className="food-pill"
                variants={fadeUp}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true }}
                custom={i * 0.5}
                whileHover={{ y: -4, scale: 1.03 }}
              >
                <span className="food-pill__emoji">{food.emoji}</span>
                <span className="food-pill__name">{food.name}</span>
                <span className="food-pill__cal">{food.cal}</span>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ── How it works ───────────────────────── */}
      <section className="section steps-section" aria-label="How it works">
        <div className="section__inner">
          <motion.h2 className="section__title" variants={fadeUp} initial="hidden" whileInView="visible" viewport={{ once: true }}>
            How It Works
          </motion.h2>
          <motion.p className="section__desc" variants={fadeUp} initial="hidden" whileInView="visible" viewport={{ once: true }} custom={1}>
            Three simple steps from photo to nutrition data.
          </motion.p>

          <div className="steps-grid">
            {steps.map((step, i) => (
              <motion.div
                key={step.num}
                className="step-card"
                variants={fadeUp}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true }}
                custom={i}
              >
                <span className="step-card__num">{step.num}</span>
                <h3 className="step-card__title">{step.title}</h3>
                <p className="step-card__desc">{step.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Features ───────────────────────────── */}
      <section className="section features-section" aria-label="Features">
        <div className="section__inner">
          <motion.h2 className="section__title" variants={fadeUp} initial="hidden" whileInView="visible" viewport={{ once: true }}>
            Why NutriVision
          </motion.h2>

          <div className="features-grid">
            {features.map((f, i) => (
              <motion.div
                key={f.title}
                className="feature-card"
                variants={fadeUp}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true }}
                custom={i}
              >
                <div className="feature-card__icon">{f.icon}</div>
                <h3 className="feature-card__title">{f.title}</h3>
                <p className="feature-card__desc">{f.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ────────────────────────────────── */}
      <section className="section cta-section">
        <div className="section__inner cta-inner">
          <motion.div className="cta-box" variants={fadeUp} initial="hidden" whileInView="visible" viewport={{ once: true }}>
            <h2 className="cta-box__title">Ready to see your food's nutrition?</h2>
            <p className="cta-box__desc">
              Upload a photo now and get instant calorie estimates — it's free and private.
            </p>
            <Link to="/analyze" className="btn btn--primary btn--lg">
              Start Analyzing
              <HiOutlineArrowRight size={18} />
            </Link>
          </motion.div>
        </div>
      </section>
    </>
  )
}
