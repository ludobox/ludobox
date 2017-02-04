import React from 'react'

import NavBar from './NavBar/NavBar.jsx'

export default class App extends React.Component {

  render() {
    return (
      <span>
        <NavBar />
        <div className="main">
          {this.props.children}

        </div>
      </span>
    )
  }
}
