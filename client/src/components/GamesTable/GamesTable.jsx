import React from 'react';

import GamesFilters from "./GamesFilters.jsx";
import GamesList from "./GamesList.jsx";

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

    // let selectedRequirements = {}
    // Object.keys(requirements).forEach(d =>
    //   selectedRequirements[d] = true
    // )

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

  changeFilterStr(filterStr) {
    this.setState({ filterStr : filterStr })
  }

  selectLanguage(selectedLanguage){
    this.setState({ selectedLanguage })
  }

  changeTimeRange(e) {
    let timeRange = parseInt(e.target.value)
    this.setState({ timeRange })
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

  render = () => {
    const {games} = this.props

    const {
      showErrors,
      filterStr,
      selectedLanguage,
      selectedAges,
      selectedRequirements,
      timeRange
    } = this.state

    // parse an array of items for fab requirements to make checks easier
    let selectedItems = [];
    selectedRequirements
      .forEach( selectedValue =>
        selectedValue !== 'nothing' ?
          selectedItems = selectedItems.concat(requirements[selectedValue].items)
        :
          selectedItems.push('Nothing')
      )

    
    let selectedGames = games
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
         new Set([])

        return selectedAges
          .filter( age => !!ages.size ? ages.has(age) : true )
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
      .filter( g => {
        if(timeRange === 120) return true // threshold : at 2h+, show all

        return g.fabrication ?
            g.fabrication.fab_time <= timeRange
            :
            true
      })

    return(
      <div>
        <GamesFilters
          games={games}

          showErrors={showErrors}
          filterStr={filterStr}
          selectedLanguage={selectedLanguage}
          selectedRequirements={selectedRequirements}
          selectedAges={selectedAges}
          timeRange={timeRange}
          requirements={requirements}
          showErrors={showErrors}

          changeTimeRange={e=> this.changeTimeRange(e)}
          changeFilterStr={e=> this.changeFilterStr(e)}
          selectLanguage={e => this.selectLanguage(e)}
          selectAge={e => this.selectAge(e)}
          handleCheckbox={e => this.handleCheckbox(e)}
          changeFilterError={e => this.changeFilterError(e)}

          />
        <GamesList
          games={selectedGames}

          showErrors={showErrors}
          filterStr={filterStr}
          selectedLanguage={selectedLanguage}
          selectedRequirements={selectedRequirements}
          selectedAges={selectedAges}
          timeRange={timeRange}
          requirements={requirements}

          />

      </div>
    )
  }
}
