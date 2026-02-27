import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Helmet } from 'react-helmet-async'
import { motion } from 'framer-motion'
import { HiOutlineUser, HiOutlineMail, HiOutlineLockClosed, HiOutlineUserAdd } from 'react-icons/hi'
import { useAuth } from '../context/AuthContext'
import './AuthPages.css'

export default function SignupPage() {
  const { signup } = useAuth()
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    if (password !== confirm) {
      setError('Passwords do not match')
      return
    }

    setBusy(true)
    try {
      await signup(username, email, password)
      navigate('/analyze')
    } catch (err) {
      setError(err.response?.data?.error || 'Signup failed. Please try again.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <>
      <Helmet>
        <title>Create Account — NutriVision</title>
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
            <h1 className="auth-card__title">Create Account</h1>
            <p className="auth-card__subtitle">Join NutriVision to save your scan history</p>
          </div>

          {error && <div className="auth-error">{error}</div>}

          <form className="auth-form" onSubmit={handleSubmit}>
            <div className="auth-field">
              <HiOutlineUser className="auth-field__icon" />
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                minLength={3}
                autoFocus
              />
            </div>

            <div className="auth-field">
              <HiOutlineMail className="auth-field__icon" />
              <input
                type="email"
                placeholder="Email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="auth-field">
              <HiOutlineLockClosed className="auth-field__icon" />
              <input
                type="password"
                placeholder="Password (min 6 chars)"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={6}
              />
            </div>

            <div className="auth-field">
              <HiOutlineLockClosed className="auth-field__icon" />
              <input
                type="password"
                placeholder="Confirm password"
                value={confirm}
                onChange={(e) => setConfirm(e.target.value)}
                required
                minLength={6}
              />
            </div>

            <button className="auth-submit" type="submit" disabled={busy}>
              {busy ? (
                <span className="auth-spinner" />
              ) : (
                <>
                  <HiOutlineUserAdd size={18} />
                  Create Account
                </>
              )}
            </button>
          </form>

          <p className="auth-switch">
            Already have an account?{' '}
            <Link to="/login">Sign in</Link>
          </p>
        </motion.div>
      </section>
    </>
  )
}
