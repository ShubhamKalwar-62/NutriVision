import { useState, useEffect } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { HiOutlineMenu, HiOutlineX, HiOutlineClock, HiOutlineLogout } from 'react-icons/hi'
import { useAuth } from '../context/AuthContext'
import './Navbar.css'

const publicLinks = [
  { path: '/', label: 'Home' },
  { path: '/about', label: 'About' },
]

export default function Navbar() {
  const location = useLocation()
  const navigate = useNavigate()
  const { isAuthenticated, user, logout } = useAuth()
  const [scrolled, setScrolled] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)

  const navLinks = isAuthenticated
    ? [
        { path: '/', label: 'Home' },
        { path: '/analyze', label: 'Analyze' },
        { path: '/history', label: 'History' },
        { path: '/about', label: 'About' },
      ]
    : publicLinks

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  useEffect(() => {
    setMobileOpen(false)
  }, [location])

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <motion.header
      className={`navbar ${scrolled ? 'navbar--scrolled' : ''}`}
      initial={{ y: -80 }}
      animate={{ y: 0 }}
      transition={{ type: 'spring', stiffness: 120, damping: 20 }}
    >
      <nav className="navbar__inner" aria-label="Main navigation">
        <Link to="/" className="navbar__brand" aria-label="NutriVision Home">
          <img src="/logo.svg" alt="NutriVision" className="navbar__logo-img" />
          <span className="navbar__title">Nutri<span className="navbar__ai">Vision</span></span>
        </Link>

        {/* Desktop links */}
        <ul className="navbar__links">
          {navLinks.map(({ path, label }) => (
            <li key={path}>
              <Link
                to={path}
                className={`navbar__link ${location.pathname === path ? 'navbar__link--active' : ''}`}
              >
                {label}
                {location.pathname === path && (
                  <motion.span className="navbar__indicator" layoutId="nav-indicator" />
                )}
              </Link>
            </li>
          ))}
        </ul>

        {/* Auth CTA */}
        {isAuthenticated ? (
          <div className="navbar__auth">
            <span className="navbar__user">{user?.username}</span>
            <button className="navbar__logout" onClick={handleLogout} title="Sign out">
              <HiOutlineLogout size={18} />
            </button>
          </div>
        ) : (
          <div className="navbar__auth">
            <Link to="/login" className="navbar__cta-link">Sign In</Link>
            <Link to="/signup" className="navbar__cta">Get Started</Link>
          </div>
        )}

        {/* Mobile toggle */}
        <button
          className="navbar__toggle"
          onClick={() => setMobileOpen(!mobileOpen)}
          aria-label="Toggle menu"
          aria-expanded={mobileOpen}
        >
          {mobileOpen ? <HiOutlineX size={24} /> : <HiOutlineMenu size={24} />}
        </button>
      </nav>

      {/* Mobile menu */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            className="navbar__mobile"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            {navLinks.map(({ path, label }) => (
              <Link
                key={path}
                to={path}
                className={`navbar__mobile-link ${location.pathname === path ? 'navbar__mobile-link--active' : ''}`}
              >
                {label}
              </Link>
            ))}
            {isAuthenticated ? (
              <button className="navbar__mobile-cta" onClick={handleLogout}>
                Sign Out
              </button>
            ) : (
              <>
                <Link to="/login" className="navbar__mobile-link">Sign In</Link>
                <Link to="/signup" className="navbar__mobile-cta">Get Started</Link>
              </>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.header>
  )
}
