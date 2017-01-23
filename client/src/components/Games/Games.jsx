import React from 'react'

import APIClient from "../../api.js"
import GamesTable from '../GamesTable/GamesTable.jsx'

// TODO: move all data logic to a separate API file
export default class Games extends React.Component {

  constructor(props) {
    super(props)
    this.api = new APIClient()
    this.state = {
      games: []
    };
  }

  fetchGames() {
    this.api.getGames( games => this.setState({ games }));
  }

  componentDidMount() {
    this.fetchGames()
  }

  render() {
    return (
      <span>
        <h3>Games</h3>
        <p>All the games contained in the box</p>
        {
          this.state.games.length ?
          <GamesTable
            games={this.state.games}
          />
          :
          "No games available."
        }
      </span>
    )
  }
}
