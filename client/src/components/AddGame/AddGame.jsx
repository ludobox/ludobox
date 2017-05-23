import React from 'react'
import GameForm from "../GameForm/GameForm.jsx"

export default class AddGame extends React.Component {
  render() {
    const game = {
      audience : {
        number_of_players : {}
      },
      credentials : {},
      description  : {},
      fabrication  : {},
      source  : {},
      title  : null,
      timestamp_add : null,
      content_type  : null,
    }

    const files = []

    return (
      <span>
        <GameForm
          game={game}
          files={files}
        />
      </span>
    )
  }
}
