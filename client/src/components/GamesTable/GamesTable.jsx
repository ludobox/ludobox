import React from 'react';

import DownloadButton from '../RemoteGames/DownloadButton.jsx'

export default class GamesTable extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      filterStr : '',
      selectedLanguage : 'any'
    }
  }

  changeFilterStr(filterStr) {
    this.setState({ filterStr : filterStr })
  }

  selectLanguage(selectedLanguage){
    this.setState({ selectedLanguage : selectedLanguage })
  }

  render() {
    let { games } = this.props
    let { filterStr, selectedLanguage } = this.state

    let languages = games.map(g => g.audience.language)

    let languagesOptions = [...new Set(languages), 'any'] // get unique languages
      .map( lg => {
        return (
          <option key={lg} value={lg}>
            {lg}
          </option>
          )
        }
      )

    let rows = games
      .filter(g => g.title.toLowerCase().includes(filterStr))
      .filter(g =>
        selectedLanguage !== 'any' ?
          g.audience.language === selectedLanguage
        : true // show all games by default
      )
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
          placeholder="Lookup a game"
        />
        <select
          value={ selectedLanguage }
          onChange={e => this.selectLanguage(e.target.value)}
          >
          {languagesOptions}
        </select>
        <table className="twelve columns" style={{tableLayout:"fixed"}}>
            <thead>
                <tr>
                    <td>Title</td>
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
