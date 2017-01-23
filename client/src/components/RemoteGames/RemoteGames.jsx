import React from 'react'
import GamesTable from '../GamesTable/GamesTable.jsx'

import APIClient from "../../api.js"

const LUDOBOX_REMOTE_ADDRESS = "http://192.168.1.30:8080";

export default class RemoteGames extends React.Component {

  constructor(props) {
    super(props)
    const options = { baseUrl : LUDOBOX_REMOTE_ADDRESS }
    this.remoteApi = new APIClient(options);
    this.remoteAddress = options.baseUrl;

    // fetch data from the box
    this.localApi = new APIClient();

    this.state = {
      remoteGames: [],
      localGames: []
    };
  }

  fetchRemoteGames() {
    this.remoteApi.getGames(remoteGames =>  this.setState({ remoteGames }) );
  }

  fetchLocalGames() {
    this.localApi.getGames(localGames =>  this.setState({ localGames }) );
  }

  componentDidMount() {
    this.fetchRemoteGames()
    this.fetchLocalGames()
  }

  render() {

    // // check which games already exists locally on the box
    let localGamesSlugs = this.state.localGames.map( d => d.slug)
    let games = this.state.remoteGames.map( d => {
        let existsLocally = localGamesSlugs.indexOf(d.slug) != -1 ? true : false;;
        return { ...d, existsLocally}
      })

    return (
      <div>
        <h3>Remote Games</h3>
        <p>
          {`Remote server at : ${this.remoteAddress} (${this.state.remoteGames.length} games)`}
        </p>
        {
          this.state.remoteGames.length ?
          <GamesTable
            games={games}
          />
          :
          "No games available."
        }
      </div>
    )
  }


}
