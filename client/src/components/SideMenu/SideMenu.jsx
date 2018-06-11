import "./sideMenu.scss";

import React from 'react'
import { slide as Menu } from 'react-burger-menu'
import { FormattedMessage, defineMessages } from 'react-intl'


const messages = defineMessages({
  games : {
    id : 'menu.games',
    defaultMessage: 'Games'
  },
  recent : {
    id : 'menu.recent',
    defaultMessage: 'Recent'
  },
  addGame : {
    id : 'menu.addGame',
    defaultMessage: 'Add Game'
  },
  download : {
    id : 'menu.download',
    defaultMessage: 'Download'
  },
  wiki : {
    id : 'menu.wiki',
    defaultMessage: 'Wiki/Help'
  },
  about : {
    id : 'menu.about',
    defaultMessage: 'About'
  },
  contact : {
    id : 'menu.contact',
    defaultMessage: 'Contact'
  },
  profile : {
    id : 'menu.profile',
    defaultMessage: 'Profile'
  },
  logout : {
    id : 'menu.logout',
    defaultMessage: 'Logout'
  },
  login : {
    id : 'menu.login',
    defaultMessage: 'Login'
  },
  register : {
    id : 'menu.register',
    defaultMessage: 'Register'
  }
})

import SocialMedia from '../SocialMedia/SocialMedia.jsx'

export default class SideMenu extends React.Component {

  render() {

    console.log(this.props.config);

    let hasRemote = Object.keys(this.props.config).length ?
    this.props.config.config.web_server_url : true ;

    let is_auth = Object.keys(this.props.config).length ?
    this.props.config.user.is_auth : false ;

    return (
      <Menu pageWrapId={'page-wrap'} outerContainerId={'outer-container'}>
            <a className="logo-menu" href="/">
              <img src="/images/ludobox-icon.png"/>
            </a>

            <a style={{marginTop:"3em"}} href="/games">
              <FormattedMessage {...messages.games} />
            </a>
            <a href="/recent">
              <FormattedMessage {...messages.recent} />
            </a>

            {
              is_auth ?
                <a href="/create">
                  <FormattedMessage {...messages.addGame} />
                </a>
              :
              null
            }

            {
              hasRemote ?
                <a href="/download">
                  <FormattedMessage {...messages.download} />
                </a>
              :
              null
            }

            <a className="no-external" href="https://wiki.ludobox.net">
              <FormattedMessage {...messages.wiki} />
              Wiki / Help
            </a>
            <a href="/about">
              <FormattedMessage {...messages.about} />
            </a>
            <a href="/contact">
              <FormattedMessage {...messages.contact} />
            </a>

            <div className="log-actions">
              {
                is_auth ?
                <span>
                  <a href="/profile">
                    <FormattedMessage {...messages.profile} />
                  </a>
                  <a href="/logout">
                    <FormattedMessage {...messages.logout} />
                  </a>
                </span>
                :
                <span>
                  <a href="/login">
                    <FormattedMessage {...messages.login} />
                  </a>
                  <a href="/register">
                    <FormattedMessage {...messages.register} />
                  </a>
                </span>
              }
            </div>

          <footer className="menuFooter">
            <SocialMedia showNames={false}/>
          </footer>
      </Menu>
    )
  }
}
