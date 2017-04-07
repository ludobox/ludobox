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

    var gameContent = Object.keys(this.state.game)
      // .sort()
      .map( key => {

      let children;
      if (typeof this.state.game[key] === "object") {
        let li = Object.keys(this.state.game[key]).map(d => (
            this.state.game[key][d] != ""
            ?
              typeof this.state.game[key][d] !== 'object' ?
                <li key={key+d}><b>{d}</b> : {this.state.game[key][d]}</li>
                :
                null
            :
            null
        ))
        children = <ul>{li}</ul>
      } else {
        children = this.state.game[key]
      }

      return (
        <li key={key + this.state.game.slug}>
          <b>{key}</b> : {children}
        </li>
      )
    })


    return (
      <span>
        <h1>{this.state.game.title}</h1>
        <ul style = {{ listStyle : "none" }}>
          {gameContent}
        </ul>
      </span>
    )
  }
}
