import React from 'react';
import { FormattedMessage, defineMessages } from 'react-intl'

import ISO6391 from 'iso-639-1'

const styles = {
  label : {
    display: "block",
    float: "left",
    paddingRight: "10px",
    whiteSpace: "nowrap"
  }
}

const messages = defineMessages({
    tools: {
      id: 'gamesFilter.tools',
      defaultMessage: 'What do you have at hand?'
    },
    time: {
      id: 'gamesFilter.time',
      defaultMessage: 'How much time do you have?'
    },
    search: {
      id: 'gamesFilter.search',
      defaultMessage: 'Search by Title'
    },
    searchPlaceholder: {
      id: 'gamesFilter.searchPlaceholder',
      defaultMessage: 'Lookup a game'
    },
    searchPlaceholder: {
      id: 'gamesFilter.searchPlaceholder',
      defaultMessage: 'Lookup a game'
    },
    language: {
      id: 'gamesFilter.language',
      defaultMessage: 'Language'
    },
    age: {
      id: 'gamesFilter.age',
      defaultMessage: 'Age'
    },
    showErros: {
      id: 'gamesFilter.showErrors',
      defaultMessage: 'Show records with formatting errors'
    },
    showLess: {
      id: 'gamesFilter.showLess',
      defaultMessage: 'Hide Options X'
    },
    showMore: {
      id: 'gamesFilter.showMore',
      defaultMessage: 'More Options'
    }
  })

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
      isEditor,
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

    let ages = ["Children", "Teenagers", "Adults"]
      .map(d => ({name : d, value : d}))

    let ageOptions = [{name:"Any", value:"any"}, ...ages]
      .map( age => {
        return (
          <option key={age.value} value={age.value}>
            {age.name}
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
          <h5>
            <FormattedMessage {...messages.tools} />
          </h5>
          <div className="reqs">
            {requirementsOptions}
          </div>
        </div>
        <div className="row">
          <h5><FormattedMessage {...messages.time} /></h5>
            {
              timeRange == 120 ?
              "2+ hours"
              :
              `${timeRange} minutes`
            }
            <br/>
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
                  <label>
                    <FormattedMessage {...messages.search} />
                  </label>
                  <FormattedMessage {...messages.searchPlaceholder}>
                    {
                      (msg) => <input
                        type="text"
                        id="filterStrField"
                        value={ filterStr }
                        onChange={ e => this.props.changeFilterStr(e.target.value) }
                        placeholder={msg}
                      />
                    }
                </FormattedMessage>
                </div>
                <div className="two columns">
                  <label>
                    <FormattedMessage {...messages.language} />
                  </label>
                  <select
                    id="languageSelector"
                    value={ selectedLanguage }
                    onChange={e => this.props.selectLanguage(e.target.value)}
                    >
                      {languagesOptions}
                    </select>
                </div>
                <div className="four columns">
                  <label>
                    <FormattedMessage {...messages.age} />
                  </label>
                  <select
                    id="languageSelector"
                    value={ selectedAges }
                    onChange={e => this.props.selectAge(e.target.value)}
                    >
                      {ageOptions}
                    </select>
                </div>
              </div>
              {
                isEditor ?
                  <div className="row">
                    <label style={styles.label}>
                      <input
                      type="checkbox"
                      checked={showErrors}
                      onChange={ e => this.props.changeFilterError(e) }
                      />
                      <span className="label-body">
                        <FormattedMessage {...messages.showErrors} />
                      </span>
                    </label>
                  </div>
                :
                null
              }
            </section>
          :
          null
        }
        <a
          className="button"
          onClick={e => this.toggleLookup(e)}
          >
            { showLookup ?
            <FormattedMessage {...messages.showLess} />
            :
            <FormattedMessage {...messages.showMore} />
            // <i className="icono-eye"></i>
          }
        </a>
      </div>
    )
  }
}
