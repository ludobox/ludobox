import React from 'react';
import DownloadButton from '../RemoteGames/DownloadButton.jsx'
import ContentState from '../ContentState/ContentState.jsx'

import ISO6391 from 'iso-639-1'

const style = {
  label : {
    display: "block",
    float: "left",
    paddingRight: "10px",
    whiteSpace: "nowrap"
  }
}

const requirements = {
  "dunno" : {
    name : "I don't know."
  },
  "nothing" : {
    name : "Nothing."
  },
  "office" : {
    name : "Office",
    items : [ "Printers B&W", "Printers Colour", "Cissors", "Pens", "Stickers", "Ruler", "Paper Glue"]
  },
  "workshop": {
    name : "Wood/Workshop",
    items : ["Cutter", "Mechanical saw", "Hand saw", "Wood glue", "Hammer", "All purpose plier", "Welder", "Sewing machine", "Drill", "Other tools"]
  },
  "fablab" : {
    name : "Fab Lab",
    items : ["3D printers", "Laser cutter", "Micro chip computer"]
  }
}

export default class GamesTable extends React.Component {

  constructor(props) {
    super(props)

    let selectedRequirements = {}
    Object.keys(requirements).forEach(d =>
      selectedRequirements[d] = true
    )

    this.state = {
      filterStr : '',
      selectedLanguage : 'any',
      selectedAges : ["Children", "Teenagers", "Adults"],
      showLookup : false,
      timeRange : 120,
      showErrors : false,
      selectedRequirements : ["dunno"] //all checked by default
    }
  }

  toggleLookup(e) {
    this.setState({ showLookup : ! this.state.showLookup })
  }

  changeFilterStr(filterStr) {
    this.setState({ filterStr : filterStr })
  }

  selectLanguage(selectedLanguage){
    this.setState({ selectedLanguage })
  }

  changeTimeRange(e) {
    this.setState({ timeRange : parseInt(e.target.value)})
  }

  selectAge(e){
    const selectedAges = [...e.target.options]
     .filter(o => o.selected)
     .map(o => o.value)
    this.setState({ selectedAges })
  }

  handleCheckbox(e) {
    let { selectedRequirements } = this.state
    let elt = e.target.name
    let state = e.target.checked

    // check if the thing is inside and remove it
    let i = selectedRequirements.indexOf(elt)
    if(i > -1) {
      selectedRequirements.splice(i, 1);
    }
    else {
      selectedRequirements.push(elt);
    }
    this.setState({ selectedRequirements })

  }

  changeFilterError() {
    let showErrors = ! this.state.showErrors
    this.setState({ showErrors })
  }

  render() {
    let { games } = this.props
    let {
      showErrors,
      showLookup,
      filterStr,
      selectedLanguage,
      selectedAges,
      timeRange,
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

    let requirementsOptions = Object.keys(requirements)
      .map( value => {
        let option = requirements[value]
        return (
          <label
            key={value}
            style={{
              display: "block",
              float: "left",
              paddingRight: "10px",
              whiteSpace: "nowrap"
            }}
            title={option.items ? option.items.join("\n"): option.name}
            htmlFor={value}
            >
            <input
              onClick={(e) => this.handleCheckbox(e)}
              title={option.items ? option.items.join("\n"): option.name}
              type='checkbox'
              name={value}
              id={value}
              defaultChecked={this.state.selectedRequirements.includes(value)}
            />
            <span className="label-body">
              {option.name}
            </span>
          </label>
          )
        }
      )

    // parse an array of items for fab requirements to make checks easier
    let selectedItems = [];
    selectedRequirements
      .forEach( selectedValue =>
        selectedValue !== 'nothing' ?
          selectedItems = selectedItems.concat(requirements[selectedValue].items)
        :
          selectedItems.push('Nothing')
      )
    // console.log(selectedItems);


    let rows = games
      .filter(g => g.title.toLowerCase().includes(filterStr))
      .filter(g =>
        selectedLanguage !== 'any' ?
          g.audience.language === selectedLanguage
        : true // show all games by default
      )
      .filter(g =>
        ! showErrors ?
          typeof g.errors === 'undefined'
          :
          true
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
          : new Set([""])

        // if "don't know" is checked
        if(selectedRequirements.includes("dunno"))
          return true

        // at least one element match
        let isSelected = false;
          reqs.forEach( r=>
            selectedItems.includes(r) ? isSelected = true : false
          )
        return isSelected
      })
      .filter( g =>
        g.fabrication ?
            g.fabrication.fab_time <= timeRange
            :
            true
      )
      .map( game => (
        <tr style={ game.existsLocally ? { background : "yellow" } : {}  }
          key={game.slug}>
          <td>
            <a
              href={"/games/"+game.slug}
              title={game.description.summary}
              >
              {game.title}
            </a>
          </td>

          <td>{
            game.audience ?
              ISO6391.getName(game.audience.language)  //
              : null
            }
          </td>
          <td>
            <a style={{textDecoration: "none"}}
              href={"/games/"+game.slug}>
                <ContentState state={game.state} errors={game.errors} />
            </a>
          </td>
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
          <label>What do you have at hand?</label>
          {requirementsOptions}
        </div>
        <div className="row">
          <label>How much time do you have?
          </label>
            {
              timeRange == 120 ?
              "2+ hours"
              :
              `${timeRange} minutes`
            }
            <input
              type="range"
              min="0"
              value={timeRange}
              max="120"
              step="10"
              onChange={ e => this.changeTimeRange(e)}
            />
        </div>
        {
          showLookup ?
          <section>
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
              <label style={style.label}>
                <input
                type="checkbox"
                checked={showErrors}
                onChange={ e => this.changeFilterError() }
                />
                <span className="label-body">
                  Show records with formatting errors
                </span>
              </label>
            </div>
          </section>
          :
          null
        }
        <a
          className="button"
          onClick={e => this.toggleLookup(e)}
          >
            { showLookup ?
            "X"
            :
            "More Options"
            // <i className="icono-eye"></i>
          }
        </a>
        <table className="twelve columns" style={{tableLayout:"fixed"}}>
            <thead>
                <tr>
                    <td>Title</td>
                    {/* <td>Fab Time</td> */}
                    <td>Language</td>
                    <td>Status</td>
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
