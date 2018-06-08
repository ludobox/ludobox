import React from 'react'
import { IntlProvider } from 'react-intl'

import { messages } from '../i18n.js'
import Selector from './Form/Selector.jsx'

const style = {
  maxWidth : '60px',
  position : 'fixed',
  bottom : '3vh',
  left : '3vh'
}

class LanguageSwitch extends React.Component {
  constructor(props) {
    super(props)
    console.log(props);
    this.state = {
      locale : props.initialLocale,
      messages : props.initialMessages
    }
    this.handleChange = this.handleChange.bind(this)
  }

  handleChange(value) {
    this.setState({ locale : value })
    this.setState({ messages : messages[value] })
  }

  render() {
    const menuItems = Object.keys(messages).map( language =>
      <a href="#"
        style={{
          padding:'1em'
        }}
        onClick={ (e) => {e.preventDefault(); this.handleChange(language)}}
        key={language}
        >
        {language}
      </a>
    )

    return (
      <div>
        <div id="language-switch" style={{
            textAlign:'right',
            position: 'absolute',
            right: '.3em',
            top: '1em',
            zIndex : '1000'
          }}>
           {menuItems}
        </div>
        <IntlProvider {...this.state}>
          <span>
            {this.props.children}
          </span>
        </IntlProvider>
      </div>
      )
  }
}

LanguageSwitch.propTypes = {
  initalLocale: React.PropTypes.oneOf(Object.keys(messages)),
  initialMessages: React.PropTypes.object
}

LanguageSwitch.defaultProps = {
  initialLocale: navigator.locale || 'en',
  initialMessages : messages['en']
}

export default LanguageSwitch
