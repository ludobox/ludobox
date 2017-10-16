import React from 'react'
import io from 'socket.io-client'

const url =
  (typeof window !== 'undefined') ? // for testing without a browser
    location.port ? '//' + document.domain + ':' + location.port : '//' + document.domain
  :
  null;

import NavBar from './NavBar/NavBar.jsx'
import APIClient from "../api.js"

export default class App extends React.Component {

  constructor(props) {
    super(props)
    this.api = new APIClient()
    this.state = {
      config: {},
      user : {}
    };
    this.socket = io.connect(url);
  }

  componentDidMount() {
    // this.api.getInfo( config => );
    let { user } = window.initialData
    this.setState({ user })
    this.setState({ config : window.initialData })

    this.socket.on('connect', function() {
        console.log("Socket.io connected. App mounted.")
    });
  }

  render() {
    // pass API children
    const childrenWithProps = React.Children.map(this.props.children,
     (child) => React.cloneElement(child, {
       api: this.api,
       config : this.state.config,
       user : this.state.user,
       socket : this.socket
     })
    );

    return (
      <span>
        <NavBar config={this.state.config}/>
        <div className="main container">
          {childrenWithProps}
        </div>
      </span>
    )
  }
}
