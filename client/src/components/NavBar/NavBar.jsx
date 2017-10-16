import "./navBar.scss";

import React from 'react'
import { slide as Menu } from 'react-burger-menu'


export default class NavBar extends React.Component {

  render() {

    let hasRemote = Object.keys(this.props.config).length ?
    this.props.config.config.web_server_url : true ;

    let is_auth = Object.keys(this.props.config).length ?
    this.props.config.user.is_auth : false ;

    return (
      <Menu pageWrapId={'page-wrap'} outerContainerId={'outer-container'}>
            <a className="navbar-link" href="/">Ludobox</a>
            <a className="navbar-link" href="/games">Games</a>
            <a className="navbar-link" href="/recent">Recent</a>
            {
              is_auth ?
                <a className="navbar-link" href="/create">Add game</a>
              :
              null
            }
            {
              hasRemote ?
                <a className="navbar-link" href="/download">Download</a>
              :
              null
            }

            <a className="navbar-link" href="/about">About</a>
            <a className="navbar-link" href="/help">Help</a>
            <a disabled className="navbar-link" href="" style={{color:"#ccc", pointerEvents: "none", cursor: "default"}}>v{this.props.config.version}</a>

            {/* {
              is_auth ?
              <span className="logged_in">
                <a className="navbar-link" href="/profile">Profile</a>
                <a className="navbar-link" href="/logout">Logout</a>
              </span>
              :
              <a className="navbar-link" href="/login">Login</a>
            } */}
      </Menu>
    )
  }
}
