import React from 'react'

import EditableText from '../Form/EditableText.jsx'
import FreeTagging from '../Form/FreeTagging.jsx'
import MultiSelect from '../Form/MultiSelect.jsx'
import Selector from '../Form/Selector.jsx'
import Number from '../Form/Number.jsx'
import FilesList from '../Form/FilesList.jsx'

import ISO6391 from 'iso-639-1'

const licenses = ["CC0", "CC BY-NC-SA 4.0", "Public Domain", "No License", "Unknown"]


const years = Array(50).fill(0).map( (d,i) => new Date().getFullYear() - i ) // 50 last years
const ages = ["Children", "Teenagers", "Adults"]
const languages = ISO6391.getAllCodes()

export default class GameBody extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      game : this.props.game,
      editMode : false,
      prevGame : null
    }
  }

  sendChanges() {
    console.log("changes are sent to server")
    console.log(this.state.game);

    this.setState({
      editMode : false
    })

  }

  cancelChanges() {
    console.log("changes cancelled")
    this.setState({
      game : Object.assign({}, this.state.prevGame),
      prevGame : null,
      editMode : false
    })
  }

  handleEditToggle() {
    this.setState({
      editMode : !this.state.editMode,
      prevGame : JSON.parse(JSON.stringify(this.state.game)) // add a backup
    })
  }

  handleSendChanges() {
    this.updateGameData()
  }

  render() {
    // console.log(this.props.game);

    const {
      audience,
      credentials,
      description ,
      fabrication ,
      source ,
      timestamp_add,
      title ,
      content_type ,
    } = this.state.game

    const { editMode } = this.state

    let editButtonStyle = {
      fontSize:"10pt",
      cursor : "pointer"
    }
    let editButton = editMode ?
      <span>
        <a onClick={() => this.sendChanges()}
          style={editButtonStyle}
          >
          <i className="icono-check"></i>
        </a>
        <a onClick={() => this.cancelChanges()}
          style={editButtonStyle}
          >
          <i className="icono-cross"></i>
        </a>
      </span>
      :
      <a
        onClick={() => this.handleEditToggle()}
        style={editButtonStyle}
        >
        <i className="icono-gear"></i>(EDIT)
      </a>

    return (
      <div>
        {editButton}
        <h1>
          <EditableText
            type="input"
            text={title}
            editing={editMode}
            handleChange={ d => {
              let game  = this.state.game
              game.title = d
              this.setState({ game });
            }}
            />
        </h1>

          {/*
            // TODO : themes and genres
            <FreeTagging
            items={ description.themes.concat(description.genres)}
            editing={editMode}
            handleChange={ d => {
              let game  = this.state.game
              game.description.themes = d.items
              this.setState({ game });
            }}
          /> */}

          <EditableText
            type="textarea"
            text={description.summary}
            editing={editMode}
            handleChange={ d => {
              let game  = this.state.game
              game.description.summary = d
              this.setState({ game });
            }}
            />
        <p>
            Webpage:
            { !editMode ?
              <a href={source.url} target="_blank">
                {source.url}
              </a>
              :
              <EditableText
               type="input"
               text={source.url}
               editing={editMode}
               handleChange={ d => {
                 let game  = this.state.game
                 game.source.url = d
                 this.setState({ game });
               }}
               />
              }
          <br/>
          Under license :
          <Selector
            editing={editMode}
            value={credentials.license}
            options={licenses}
            handleChange={ d => {
              let game  = this.state.game
              game.credentials.license = d
              this.setState({ game });
            }}
          />
          <br/>
          Published in :
          <Selector
            editing={editMode}
            value={credentials.publication_year}
            options={years}
            handleChange={ d => {
              let game  = this.state.game
              game.credentials.publication_year = d
              this.setState({ game });
            }}
          />

        </p>
        <hr/>

        <div className="row">
          <div className="six columns">
            <p>
              Language:
              <Selector
                editing={editMode}
                value={audience.language}
                options={languages}
                handleChange={ d => {
                  let game  = this.state.game
                  game.audience.language = d
                  this.setState({ game });
                }}
              />

              <br/>
              Number of players :
              { editMode ? " (minimum)" : null}
              <Number
                editing={editMode}
                value={audience.number_of_players.players_min}
                handleChange={ d => {
                  let game  = this.state.game
                  game.audience.number_of_players.players_min = d
                  this.setState({ game });
                }}
              />
               -
              { editMode ? "Number_of_players (maximum)" : null}
              <Number
                editing={editMode}
                value={audience.number_of_players.players_max}
                handleChange={ d => {
                  let game  = this.state.game
                  game.audience.number_of_players.players_max = d
                  this.setState({ game });
                }}
              />
              <br/>
            Duration of each play (minutes):
            <Number
              editing={editMode}
              value={audience.duration}
              handleChange={ d => {
                let game  = this.state.game
                game.audience.duration = d
                this.setState({ game });
              }}
            />
            </p>
          </div>
          <div className="six columns">
            <MultiSelect
              value={audience.age}
              options={ages}
              editing={editMode}
              handleChange={ d => {
                let game  = this.state.game
                game.audience.age = d
                this.setState({ game });
              }}
            />
          </div>
        </div>

        <hr/>

        <div className="row">
          <div className="six columns">
            { ! editMode ?
              <h5>Fabrication time : {fabrication.fab_time} minutes </h5>
              :
              <p>
                Fabrication time (minutes):
                <Number
                  editing={editMode}
                  defaultValue={fabrication.fab_time}
                  fieldId="fabrication.fab_time"
                  handleChange={ d => {
                    let game  = this.state.game
                    game.fabrication.fab_time = d
                    this.setState({ game });
                  }}
              />
              </p>
            }
            <MultiSelect
              options={["ha"]}
              value={fabrication.requirements}
            />
          </div>
          <div className="six columns">
            <h5>Download files</h5>
            <FilesList
              files={this.props.files}
            />
          </div>
        </div>

        <hr/>

        <div className="row">
          <div className="four columns">
            <p>Authors</p>
            {/* <Number

              defaultValue={fabrication.fab_time}
              fieldId="fabrication.fab_time"
            />
             */}
            <FreeTagging
              items={credentials.authors}
              editing={editMode}
              handleChange={ d => {
                let game  = this.state.game
                game.credentials.authors = d
                this.setState({ game });
              }}
            />
          </div>
          <div className="four columns">
            <p>Illustrators</p>
            <FreeTagging
              items={credentials.illustrators}
              editing={editMode}
              handleChange={ d => {
                let game  = this.state.game
                game.credentials.illustrators = d
                this.setState({ game });
              }}
            />
          </div>
          <div className="four columns">
            <p>Publishers</p>
            <FreeTagging
              items={credentials.publishers}
              editing={editMode}
              handleChange={ d => {
                let game  = this.state.game
                game.credentials.publishers = d
                this.setState({ game });
              }}
            />
          </div>
        </div>

        <hr/>

        <p>{content_type} added on {timestamp_add}.</p>
      </div>
    )
  }
}

// helper from http://stackoverflow.com/questions/6491463/accessing-nested-javascript-objects-with-string-key

Object.byString = function(o, s) {
    s = s.replace(/\[(\w+)\]/g, '.$1'); // convert indexes to properties
    s = s.replace(/^\./, '');           // strip a leading dot
    var a = s.split('.');
    for (var i = 0, n = a.length; i < n; ++i) {
        var k = a[i];
        if (k in o) {
            o = o[k];
        } else {
            return;
        }
    }
    return o;
}
