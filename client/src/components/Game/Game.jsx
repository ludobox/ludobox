import React from 'react'

export default class Game extends React.Component {

  render() {
    return (
      <span>
        <p>Display a single game</p>
        <h1>{this.props.game.title}</h1>
      </span>
    )
  }
}
