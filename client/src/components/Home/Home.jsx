import React from 'react'

export default class Home extends React.Component {

  render() {
    return (
      <span>
        <h3>Hello !</h3>
        <p>Welcome to Ludobox :)</p>
        <p>What would you like to do ?</p>
        <ul>
          <li>
            <a href="/games">Browse games</a>
          </li>
          <li>
            <a href="/create">Create a new game</a>
          </li>
          <li>
            <a href="/download">Download more games</a>
          </li>
          <li>
            <a href="/about">Learn more about the Ludobox project</a>
          </li>
        </ul>
      </span>
    )
  }
}
