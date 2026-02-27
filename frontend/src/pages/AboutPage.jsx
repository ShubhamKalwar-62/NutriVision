import { Helmet } from 'react-helmet-async'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { HiOutlineArrowRight } from 'react-icons/hi'
import './AboutPage.css'

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.1, duration: 0.5, ease: [0.22, 1, 0.36, 1] },
  }),
}

const pipeline = [
  {
    step: 'Image Input',
    detail: 'User uploads a food image (with thumb for scale). The image is resized to 608×608 for the model.',
  },
  {
    step: 'YOLOv4 Detection',
    detail: 'Custom-trained YOLOv4 detects food items and thumb with 98.6% accuracy using Non-Maximum Suppression.',
  },
  {
    step: 'Segmentation',
    detail: 'Adaptive thresholding + contour extraction isolates each detected item from the background.',
  },
  {
    step: 'Size Calibration',
    detail: 'Thumb detection provides pixel-to-cm conversion — a known thumb size (5 × 2.3 cm) maps pixels to real-world dimensions.',
  },
  {
    step: 'Volume Estimation',
    detail: 'Spherical model for round fruits (apple, orange, tomato) and cylindrical model for elongated items (banana, carrot).',
  },
  {
    step: 'Calorie Calculation',
    detail: 'Volume × density = mass, then (calories per 100g / 100) × mass = estimated total calories.',
  },
]

const techStack = [
  { name: 'YOLOv4', desc: 'Object detection model trained on custom food + thumb dataset' },
  { name: 'OpenCV', desc: 'Image processing, DNN inference, segmentation, and contour analysis' },
  { name: 'Flask', desc: 'Lightweight Python API server serving the model over REST' },
  { name: 'React + Vite', desc: 'Modern, fast frontend with smooth animations via Framer Motion' },
  { name: 'Deep Learning', desc: 'Darknet-based architecture with 98.6% mAP after 3000 iterations' },
]

export default function AboutPage() {
  return (
    <>
      <Helmet>
        <title>About — NutriVision Technical Deep Dive</title>
        <meta
          name="description"
          content="Learn how NutriVision uses YOLOv4, OpenCV, and computer vision to detect food items and estimate calories from a single photo."
        />
      </Helmet>

      <section className="about">
        <div className="about__inner">
          {/* Header */}
          <motion.div className="about__header" variants={fadeUp} initial="hidden" animate="visible" custom={0}>
            <h1 className="about__title">About NutriVision</h1>
            <p className="about__subtitle">
              A complete pipeline from food photo to calorie estimation — powered by deep learning,
              computer vision, and geometric modeling.
            </p>
          </motion.div>

          {/* Pipeline */}
          <motion.div variants={fadeUp} initial="hidden" animate="visible" custom={1}>
            <h2 className="about__section-title">Processing Pipeline</h2>
            <div className="pipeline">
              {pipeline.map((p, i) => (
                <motion.div
                  key={p.step}
                  className="pipeline__card"
                  variants={fadeUp}
                  initial="hidden"
                  whileInView="visible"
                  viewport={{ once: true }}
                  custom={i}
                >
                  <span className="pipeline__num">{String(i + 1).padStart(2, '0')}</span>
                  <div>
                    <h3 className="pipeline__step">{p.step}</h3>
                    <p className="pipeline__detail">{p.detail}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Tech stack */}
          <motion.div variants={fadeUp} initial="hidden" whileInView="visible" viewport={{ once: true }} custom={2}>
            <h2 className="about__section-title">Technology Stack</h2>
            <div className="tech-grid">
              {techStack.map((t) => (
                <div key={t.name} className="tech-card">
                  <h4 className="tech-card__name">{t.name}</h4>
                  <p className="tech-card__desc">{t.desc}</p>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Supported foods table */}
          <motion.div variants={fadeUp} initial="hidden" whileInView="visible" viewport={{ once: true }} custom={3}>
            <h2 className="about__section-title">Nutrition Reference Data</h2>
            <div className="about__table-wrap">
              <table className="about__table">
                <thead>
                  <tr>
                    <th>Food</th>
                    <th>Density (g/cm³)</th>
                    <th>Calories (kcal/100g)</th>
                    <th>Shape Model</th>
                  </tr>
                </thead>
                <tbody>
                  <tr><td>🍎 Apple</td><td>0.96</td><td>52</td><td>Sphere</td></tr>
                  <tr><td>🍌 Banana</td><td>0.94</td><td>89</td><td>Cylinder</td></tr>
                  <tr><td>🥕 Carrot</td><td>0.641</td><td>41</td><td>Cylinder</td></tr>
                  <tr><td>🧅 Onion</td><td>0.513</td><td>40</td><td>Sphere</td></tr>
                  <tr><td>🍊 Orange</td><td>0.482</td><td>47</td><td>Sphere</td></tr>
                  <tr><td>🥝 Kiwi</td><td>0.575</td><td>44</td><td>Sphere</td></tr>
                  <tr><td>🍅 Tomato</td><td>0.481</td><td>18</td><td>Sphere</td></tr>
                </tbody>
              </table>
            </div>
          </motion.div>

          {/* CTA */}
          <motion.div className="about__cta" variants={fadeUp} initial="hidden" whileInView="visible" viewport={{ once: true }}>
            <Link to="/analyze" className="btn btn--primary btn--lg">
              Try It Now
              <HiOutlineArrowRight size={18} />
            </Link>
          </motion.div>
        </div>
      </section>
    </>
  )
}
