import React from 'react'

export default class Home extends React.Component {

  render() {

    let hasRemote = Object.keys(this.props.config).length ?
    this.props.config.config.web_server_url : true ;

    return (
        <div className="row">
          <div className="six columns">
            <img
              className="ludobox-logo"
              src="/images/ludobox-logo-color2.png"
            />
          </div>
          <div className="six columns" style={{ textAlign : 'center', 'paddingTop' : '2em'}}>
            <h3 className="welcome">
              Welcome to {this.props.config.name ? this.props.config.name: "Ludobox"}
            </h3>
            <p>What would you like to do ?</p>
            <ul style={{ listStyle : 'none' }}>
              <li>
                <a className="button button-primary" href="/games">Browse games</a>
              </li>
              <li>
                <a className="button" href="/create">Add a new game</a>
              </li>
              {
                hasRemote ?
                <li>
                  <a className="button" href="/download">Download more games</a>
                </li>
                :
                null
              }
              <li>
                <a className="button" href="/about">Learn about Ludobox</a>
              </li>
            </ul>
          </div>
        </div>
    )
  }
}
