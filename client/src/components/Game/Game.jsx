import React from 'react'
import APIClient from "../../api.js"
import GameBody from "./GameBody.jsx"

export default class Game extends React.Component {

  constructor(props) {
    super(props)
    this.api = new APIClient()
    this.state = {
      game: null,
      files: []
    };
  }

  fetchGame(slug) {
    this.api.getGame(slug, game => this.setState({ game }));
  }

  fetchFiles(slug) {
    this.api.getGameFilesList(slug, files => this.setState({ files }));
  }

  componentDidMount() {
    this.fetchGame(this.props.params.gameSlug)
    this.fetchFiles(this.props.params.gameSlug)
  }

  render() {

    return (
      <span>
        { this.state.game && this.state.files ?
          <GameBody
            game={this.state.game}
            files={this.state.files}
          />
          :
          null
        }
      </span>
    )
  }
}
