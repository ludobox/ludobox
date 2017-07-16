import React from 'react'

import APIClient from "../../api.js"
import GameForm from "../GameForm/GameForm.jsx"
import ActionButtons from "../ActionButtons/ActionButtons.jsx"

// import History from "../History/History.jsx"

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
        url : this.api.getURL(`games/${slug}/files/${f}`),
        filename : f
      }))
      this.setState({ game, files })
    });
  }

  componentDidMount() {
    this.fetchGame(this.props.params.gameSlug)
  }

  render() {
    let {files, game} = this.state
    return (
      <div>
      {
        game && files ?
        <span>
          <GameForm
            game={game}
            editMode={false}
            files={files}
            errors={{}} // defaultProps to empty object
          />
          <ActionButtons
            slug={game.slug}
            user={this.props.user}
            />
        </span>
        :
        null
      }
    </div>
    )
  }

}
