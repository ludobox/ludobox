import React from 'react'
import io from 'socket.io-client'

const url =
  (typeof window !== 'undefined') ? // for testing without a browser
    location.port ? 'http://' + document.domain + ':' + location.port : 'http://' + document.domain
  :
  null;

import NavBar from './NavBar/NavBar.jsx'
import APIClient from "../api.js"

export default class App extends React.Component {

  constructor(props) {
    super(props)
    this.api = new APIClient()
    this.socket = io.connect(url);
  }

  componentDidMount() {
    // this.api.getInfo( config => this.setState({ config }));
    this.socket.on('connect', function() {
        console.log("Socket.io connected. App mounted.")
    });
  }

  render() {


    // pass API children
    const childrenWithProps = React.Children.map(this.props.children,
     (child) => React.cloneElement(child, {
       api: this.api,
       config : window.initialData.config,
       user : window.initialData.user,
       socket : this.socket
     })
    );

    return (
      <span>
        <NavBar config={this.state.config}/>
        <div className="main">
          {childrenWithProps}
        </div>
      </span>
    )
  }
}
