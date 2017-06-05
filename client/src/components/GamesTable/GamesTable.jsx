import React from 'react';
import DownloadButton from '../RemoteGames/DownloadButton.jsx'

import ISO6391 from 'iso-639-1'


const requirements = [
  {
    name : "Nothing.",
    value : "nothing"
  },
  {
    name : "Office (printer)",
    value : "print"
  },
  {
    name : "Wood Workshop (saw, hammer...)",
    value : "wood"
  },
  {
    name : "Fab Lab (3D printer, lasercutter...)",
    value : "fablab"
  }
]

export default class GamesTable extends React.Component {

  constructor(props) {
    super(props)

    let selectedRequirements = {}
    requirements.forEach(d =>
      selectedRequirements[d.value] = true
    )

    this.state = {
      filterStr : '',
      selectedLanguage : 'any',
      selectedAges : ["Children", "Teenagers", "Adults"],
      selectedRequirements : selectedRequirements
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

  handleCheckbox(e) {
    let { selectedRequirements } = this.state
    selectedRequirements[e.target.name] = e.target.checked
    this.setState({ selectedRequirements })
  }

  render() {
    let { games } = this.props
    let { filterStr,
      selectedLanguage,
      selectedAges,
      selectedRequirements
    } = this.state

    // get unique language codes
    let lgg = new Set(games.map(g => g.audience.language))

    // get screen names
    let languages = ISO6391.getLanguages(Array.from(lgg))

    let languagesOptions = [
      { name: 'Any', code : 'any'},
      ...languages
    ]
      .map( lg => {
        return (
          <option key={lg.code} value={lg.code}>
            {lg.name}
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

    let requirementsOptions = requirements
      .map( option => {
        return (
          <label
            key={option.value}
            style={{
              display: "block",
              float: "left",
              paddingRight: "10px",
              whiteSpace: "nowrap"
            }}
            >
            <input
              onClick={(e) => this.handleCheckbox(e)}
              type='checkbox'
              name={option.value}
              defaultChecked={this.state.selectedRequirements[option.value]}
            />
            <span className="label-body">
              {option.name}
            </span>
          </label>
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
      .filter(g => {
        let reqs = g.fabrication && g.fabrication.requirements ?
          new Set(g.fabrication.requirements)
          :
          new Set([""])

        console.log(selectedRequirements)
        return Object.keys(selectedRequirements)
          .filter( d => selectedRequirements[d] )
          .filter( req => reqs.has(req) )
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
        <div className="row">
          <label>What do you have at hand?</label>
          {requirementsOptions}
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
