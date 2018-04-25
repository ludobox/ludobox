import React from 'react'

import APIClient from "../../api.js"

import PageTitle from '../PageTitle/PageTitle.jsx'
import GamesTable from '../GamesTable/GamesTable.jsx'


// TODO: move all data logic to a separate API file
export default class Games extends React.Component {

  constructor(props) {
    super(props)
    this.api = new APIClient()
    this.state = {
      games: [],
      gamesReady: false
    };
  }

  fetchGames() {
    this.api.getGames( games => this.setState({ games, gamesReady: true }));
  }

  componentDidMount() {
    this.fetchGames()
  }

  render() {

    const {games, gamesReady} = this.state

    return (
      <span>
        <PageTitle />
        {
          gamesReady ?
            this.state.games.length ?
            <GamesTable
              games={games}
              user={this.props.user}
            />
            :
            "No games available."
          :
           "Loading..."
        }
      </span>
    )
  }
}
