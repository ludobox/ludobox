import React from 'react'

const style = {
  marginBottom : "2em"
}

export default class NavBar extends React.Component {

  render() {

    let hasRemote = Object.keys(this.props.config).length ?
    this.props.config.config.web_server_url : true ;

    let is_auth = Object.keys(this.props.config).length ?
    this.props.config.user.is_auth : false ;

    return (
      <nav className="navbar" style={style}>
        <div className="container">
          <ul className="navbar-list">
            <li className="navbar-item ludobox-nav-header"><a className="navbar-link" href="/">Ludobox</a></li>
            <li className="navbar-item"><a className="navbar-link" href="/games">Games</a></li>
            <li className="navbar-item">
              <a className="navbar-link" href="/create">Add game</a>
            </li>
            {
              hasRemote ?
              <li className="navbar-item">
                <a className="navbar-link" href="/download">Download</a>
              </li>
              :
              null
            }
            <li className="navbar-item"><a className="navbar-link" href="/about">About</a></li>
            <li className="navbar-item"><a className="navbar-link" href="/help">Help</a></li>
            <li className="navbar-item"><a disabled className="navbar-link" href="" style={{color:"#ccc", pointerEvents: "none", cursor: "default"}}>v{this.props.config.version}</a></li>

            {
              is_auth ?
              <li className="navbar-item"><a className="navbar-link" href="/logout">Logout</a></li>
              :
              <li className="navbar-item"><a className="navbar-link" href="/login">Login</a></li>
            }
          </ul>
        </div>
      </nav>
    )
  }
}
