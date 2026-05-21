import { Link, useLocation } from 'react-router-dom'

export function Header() {
  const { pathname } = useLocation()

  return (
    <header className="header">
      <Link to="/" className="header-logo">
        <div className="header-logo-icon">⚡</div>
        <span className="header-logo-text">API Executor <span>with File Data</span></span>
      </Link>
      <nav className="header-nav">
        <Link to="/" className={`nav-link ${pathname === '/' ? 'active' : ''}`}>Agents</Link>
      </nav>
    </header>
  )
}
