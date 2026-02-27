import { Link } from 'react-router-dom'
import { FaGithub } from 'react-icons/fa'
import './Footer.css'

export default function Footer() {
  return (
    <footer className="footer" role="contentinfo">
      <div className="footer__inner">
        <div className="footer__brand">
          <img src="/logo.svg" alt="NutriVision" className="footer__logo-img" />
          <div>
            <p className="footer__name">NutriVision</p>
            <p className="footer__tagline">Deep Learning Calorie Estimation</p>
          </div>
        </div>

        <nav className="footer__links" aria-label="Footer navigation">
          <Link to="/">Home</Link>
          <Link to="/analyze">Analyze</Link>
          <Link to="/history">History</Link>
          <Link to="/about">About</Link>
        </nav>

        <div className="footer__social">
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="GitHub"
          >
            <FaGithub size={20} />
          </a>
        </div>
      </div>

      <div className="footer__bottom">
        <p>&copy; {new Date().getFullYear()} NutriVision. Built with YOLOv4 &amp; React.</p>
      </div>
    </footer>
  )
}
