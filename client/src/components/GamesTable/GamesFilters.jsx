import React from 'react';

import ISO6391 from 'iso-639-1'

const styles = {
  label : {
    display: "block",
    float: "left",
    paddingRight: "10px",
    whiteSpace: "nowrap"
  }
}


export default class GamesFilters extends React.Component {

  constructor(props) {
    super(props)
    this.state = { showLookup : false }
  }

  toggleLookup(e) {
    this.setState({ showLookup : ! this.state.showLookup })
  }

  render() {

    const {showLookup} = this.state

    let {
      games,
      showErrors,
      filterStr,
      selectedLanguage,
      selectedAges,
      timeRange,
      requirements,
      selectedRequirements
    } = this.props

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

    let ageOptions = ["Children", "Teenagers", "Adults"]
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
              onClick={(e) => this.props.handleCheckbox(e)}
              title={option.items ? option.items.join("\n"): option.name}
              type='checkbox'
              name={value}
              id={value}
              defaultChecked={selectedRequirements.includes(value)}
            />
            <span className="label-body">
              {
                option.icon ?
                  <img className="req-icon" src={option.icon}/>
                :
                  null
              }
              <br />
              {option.name}
            </span>
          </label>
          )
        }
      )

    return (
      <div className="filters">
        <div className="row">
          <label>What do you have at hand?</label>
          <div className="reqs">
            {requirementsOptions}
          </div>
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
              onChange={ e => this.props.changeTimeRange(e)}
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
                    onChange={ e => this.props.changeFilterStr(e.target.value) }
                    placeholder="Lookup a game"
                  />
                </div>
                <div className="two columns">
                  <label>Language</label>
                  <select
                    id="languageSelector"
                    value={ selectedLanguage }
                    onChange={e => this.props.selectLanguage(e.target.value)}
                    >
                      {languagesOptions}
                    </select>
                </div>
                <div className="four columns">
                  <label>Age</label>
                  <select
                    id="languageSelector"
                    value={ selectedAges }
                    onChange={e => this.props.selectAge(e)}
                    multiple
                    >
                      {ageOptions}
                    </select>
                </div>
              </div>
              <div className="row">
                <label style={styles.label}>
                  <input
                  type="checkbox"
                  checked={showErrors}
                  onChange={ e => this.props.changeFilterError(e) }
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
      </div>
    )
  }
}
