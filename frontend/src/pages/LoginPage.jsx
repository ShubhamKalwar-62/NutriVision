import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Helmet } from 'react-helmet-async'
import { motion } from 'framer-motion'
import { HiOutlineMail, HiOutlineLockClosed, HiOutlineLogin } from 'react-icons/hi'
import { useAuth } from '../context/AuthContext'
import './AuthPages.css'

export default function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setBusy(true)
    try {
      await login(email, password)
      navigate('/analyze')
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed. Please try again.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <>
      <Helmet>
        <title>Sign In — NutriVision</title>
      </Helmet>

      <section className="auth-page">
        <motion.div
          className="auth-card"
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="auth-card__header">
            <img src="/logo.svg" alt="NutriVision" className="auth-card__logo-img" />
            <h1 className="auth-card__title">Welcome Back</h1>
            <p className="auth-card__subtitle">Sign in to access your scan history</p>
          </div>

          {error && <div className="auth-error">{error}</div>}

          <form className="auth-form" onSubmit={handleSubmit}>
            <div className="auth-field">
              <HiOutlineMail className="auth-field__icon" />
              <input
                type="text"
                placeholder="Email or username"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                autoFocus
              />
            </div>

            <div className="auth-field">
              <HiOutlineLockClosed className="auth-field__icon" />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={6}
              />
            </div>

            <button className="auth-submit" type="submit" disabled={busy}>
              {busy ? (
                <span className="auth-spinner" />
              ) : (
                <>
                  <HiOutlineLogin size={18} />
                  Sign In
                </>
              )}
            </button>
          </form>

          <p className="auth-switch">
            Don&apos;t have an account?{' '}
            <Link to="/signup">Create one</Link>
          </p>
        </motion.div>
      </section>
    </>
  )
}
