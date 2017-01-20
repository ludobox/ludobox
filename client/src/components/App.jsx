import React from 'react'
import axios from 'axios'

import GamesIndex from './GamesIndex/GamesIndex.jsx'
import PageTitle from './PageTitle/PageTitle.jsx'

export default class App extends React.Component {

  constructor(props) {
    super(props)

    this.state = {
      localGames: [],
      remoteGames: [],
      downloading : []
    };
  }

  fetchGame(slug) {
    console.log(this);
    console.log("Download "+ slug + "...")
    this.setState({ downloading : [...this.state.downloading, slug]  })

    axios.get(`${this.props.remote_address}/api/games/${slug}/info.json`)
      .then(res => {
        var info = res.data
        console.log(info);

        // get list of files
        axios.get(`${this.props.remote_address}/api/files/${slug}`)
          .then(res => {
            var files  = res.data.map( n =>
              ({
                url : `${this.props.remote_address}/api/games/${slug}/files/${n}`,
                filename : n
              })
            );
            console.log(files);

            // save the game
            axios.post(`/api/clone`, {info, files, slug})
            .then(res => {
              console.log(res);
              this.fetchIndex()
              this.setState({
                downloading : this.state.downloading
                .splice(this.state.downloading.indexOf(slug))
               })
            })
            .catch(function (error) {
              console.log(error);
              this.setState({
                downloading : this.state.downloading
                .splice(this.state.downloading.indexOf(slug))
               })
            });

          })
          .catch(function (error) {
            console.log(error);
          });
      });
  }

  fetchIndex() {
    if (this.props.remote_address) {
      axios.get(`${this.props.remote_address}/api/games`)
        .then(res => {
          const remoteGames = res.data;
          this.setState({ remoteGames });
        });
    }

    axios.get(`/api/games`)
      .then(res => {
        const localGames = res.data;
        this.setState({ localGames });
      });
  }

  componentDidMount() {
    this.fetchIndex()
  }

  render() {

    let localGamesSlugs = this.state.localGames.map( d => d.slug)

    // check if there is a connection of not
    let remoteGames = this.state.remoteGames.map( d => {
        let existsLocally = localGamesSlugs.indexOf(d.slug) != -1 ? true : false;;
        return { ...d, existsLocally}
      })

    return (
      <span>
        <PageTitle />
        <p>
          {`Local server (${this.state.localGames.length} games)`}<br />
          {`Remote server at : ${this.props.remote_address} (${this.state.remoteGames.length} games)`}
        </p>
        <h3>Remote Games</h3>
        {
          remoteGames.length ?
            <GamesIndex
            games={remoteGames}
            url={ this.props.remote_address}
            fetchGame={this.fetchGame.bind(this)}
            downloading={this.state.downloading}
            />
          :
          "No games available."
        }
        <h3>Local Games</h3>
        {
          this.state.localGames.length ?
          <GamesIndex
            games={this.state.localGames}
          />
          :
          "No games available."
        }

      </span>
    )
  }
}
