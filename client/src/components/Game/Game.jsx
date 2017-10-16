import React from 'react'

import APIClient from "../../api.js"
import GamePage from "./GamePage.jsx"


import validator from 'is-my-json-valid'
import model from '../../../../model/game.json'

const alertOptions = {
  offset: 14,
  position: 'bottom left',
  theme: 'dark',
  time: 5000,
  transition: 'scale'
}

export default class Game extends React.Component {

  constructor(props) {
    super(props)
    this.api = new APIClient();
    this.state = {
      game: null,
      files: [],
    };
  }

  fetchGame(slug) {
    this.api.getGame(slug, game => {
      let { files } = game
      files = files.map( f => ({
        url : this.api.getURL(`files/${slug}/${f}`),
        filename : f
      }))
      this.setState({ game, files })
    });
  }

  updateContent() {
    this.fetchGame(this.props.params.gameSlug)
  }

  componentDidMount() {
    this.fetchGame(this.props.params.gameSlug)
  }

  render() {

    let {
      files,
      game
    } = this.state

    return (
      game && files ?
        <GamePage
          title={game.title}
          audience={game.audience}
          description={game.description}
          history={game.history}
          fabrication={game.fabrication}
          credentials={game.credentials}
          files={files}
          slug={game.slug}
          source={game.source}
          contentState={game.state}
          user={this.props.user}
          />
      :
        null
    )
  }

}
