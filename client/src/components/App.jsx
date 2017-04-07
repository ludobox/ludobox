import React from 'react'

import NavBar from './NavBar/NavBar.jsx'
import APIClient from "../api.js"

export default class App extends React.Component {

  constructor(props) {
    super(props)
    this.api = new APIClient()
    this.state = {
      config: {}
    };
  }

  componentDidMount() {
    this.api.getInfo( config => this.setState({ config }));
  }

  render() {
    console.log(this.state.config);

    // pass API children
    const childrenWithProps = React.Children.map(this.props.children,
     (child) => React.cloneElement(child, {
       api: this.api,
       config : this.state.config
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
