import React from 'react';
import DownloadButton from '../RemoteGames/DownloadButton.jsx'

export default class GamesTable extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      filterStr : '',
      selectedLanguage : 'any',
      selectedAges : ["Children", "Teenagers", "Adults"]
    }
  }

  changeFilterStr(filterStr) {
    this.setState({ filterStr : filterStr })
  }

  selectLanguage(selectedLanguage){
    this.setState({ selectedLanguage })
  }

  selectAge(e){
    const selectedAges = [...e.target.options]
     .filter(o => o.selected)
     .map(o => o.value)
    this.setState({ selectedAges })
  }

  render() {
    let { games } = this.props
    let { filterStr,
      selectedLanguage,
      selectedAges
    } = this.state

    let languages = games.map(g => g.audience.language)

    let languagesOptions = ['any', ...new Set(languages)] // get unique languages
      .map( lg => {
        return (
          <option key={lg} value={lg}>
            {lg}
          </option>
          )
        }
      )

    let ageOptions = ["Children", "Teenagers", "Adults", null]
      .map( age => {
        return (
          <option key={age} value={age}>
            {age}
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
      .filter(g => {
        let ages = g.audience.age ?
         new Set(g.audience.age):
         new Set([""])
        return selectedAges
          .filter( age => ages.has(age) )
          .length
      })
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
          {/* <td>{game.fabrication ? game.fabrication.fab_time : null}</td> */}
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
        <div className="row">
          <div className="six columns">
            <label>Search</label>
            <input
              type="text"
              id="filterStrField"
              value={ filterStr }
              onChange={ e => this.changeFilterStr(e.target.value) }
              placeholder="Lookup a game"
            />
          </div>
          <div className="two columns">
            <label>Language</label>
            <select
              id="languageSelector"
              value={ selectedLanguage }
              onChange={e => this.selectLanguage(e.target.value)}
              >
                {languagesOptions}
              </select>
          </div>
          <div className="four columns">
            <label>Age</label>
            <select
              id="languageSelector"
              value={ selectedAges }
              onChange={e => this.selectAge(e)}
              multiple
              >
                {ageOptions}
              </select>
          </div>
        </div>
        <table className="twelve columns" style={{tableLayout:"fixed"}}>
            <thead>
                <tr>
                    <td>Title</td>
                    {/* <td>Fab Time</td> */}
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
