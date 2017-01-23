import React from 'react'
import APIClient from "../../api.js"

export default class Game extends React.Component {


  constructor(props) {
    super(props)
    this.api = new APIClient()
    this.state = {
      game: {}
    };
  }

  fetchGame(slug) {
    this.api.getGame(slug, game => this.setState({ game }));
  }

  componentDidMount() {
    this.fetchGame(this.props.params.gameSlug)
  }
  render() {

    var gameContent = Object.keys(this.state.game).map( key => (
      <li key={key + this.state.game.slug}>
        <b>{key}</b> : {this.state.game[key]}
      </li>
    ))

    return (
      <span>
        <h1>{this.state.game.title}</h1>
        <p>{this.state.game.description}</p>
        <ul>
          {gameContent}
        </ul>
      </span>
    )
  }
}
