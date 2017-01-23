import React from 'react'

const style = {
  marginBottom : "2em"
}

export default class NavBar extends React.Component {

  render() {
    return (
      <nav className="navbar" style={style}>
        <div className="container">
          <ul className="navbar-list">
            <li className="navbar-item"><a className="navbar-link" href="/">Ludobox</a></li>
            <li className="navbar-item"><a className="navbar-link" href="/games">Games</a></li>
            <li className="navbar-item">
              <a className="navbar-link" href="/create">Add game</a>
            </li>
            <li className="navbar-item">
              <a className="navbar-link" href="/download">Download</a>
            </li>
            <li className="navbar-item"><a className="navbar-link" href="/about">About</a></li>
          </ul>
        </div>
      </nav>
    )
  }
}
