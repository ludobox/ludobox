import React from 'react';

import DownloadButton from '../RemoteGames/DownloadButton.jsx'

export default class GamesTable extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      filterStr : ''
    }
  }

  changeFilterStr(filterStr) {
    this.setState({ filterStr : filterStr })
  }

  render() {
    // console.log(this.props.games);
    let { games } = this.props
    let { filterStr } = this.state

    let rows = games
      .filter(g => g.title.toLowerCase().includes(filterStr))
      .map( game => (
        <tr style={ game.existsLocally ? { background : "yellow" } : {}  }
          key={game.slug}>
          <td>
            <a
              href={"/games/"+game.slug}
              // target="_blank"
              >
              {game.title}
            </a>
          </td>
          <td>{game.content_type}</td>
          <td>{game.fabrication ? game.fabrication.fab_time : null}</td>
          <td>{game.audience ? game.audience.language : null }</td>
          {
            ! game.existsLocally && this.props.remoteApi && this.props.localApi ?
            <td>
              <DownloadButton
                socket={this.props.socket}
                remoteApi={this.props.remoteApi}
                localApi={this.props.localApi}
                slug={game.slug}
                />
            </td>
            :
            null
          }
        </tr>
      ))

    return (
      <div>
        <input
          type="text"
          value={ filterStr }
          onChange={ e => this.changeFilterStr(e.target.value) }
        />
        <table className="twelve columns" style={{tableLayout:"fixed"}}>
            <thead>
                <tr>
                    <td>Title</td>
                    <td>Type</td>
                    <td>Fab Time</td>
                    <td>Language</td>
                    {
                      this.props.remoteApi ?
                      <td>Download</td>
                      :
                      null
                    }
                </tr>
            </thead>
            <tbody>
              {rows}
            </tbody>
        </table>
      </div>
    )
  }
}
