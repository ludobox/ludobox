import React from 'react'

import EditableText from '../Form/EditableText.jsx'
import FreeTagging from '../Form/FreeTagging.jsx'
import MultiSelect from '../Form/MultiSelect.jsx'
import Selector from '../Form/Selector.jsx'
import Number from '../Form/Number.jsx'

import ISO6391 from 'iso-639-1'

const licenses = ["CC0", "CC BY-NC-SA 4.0", "Public Domain", "No License", "Unknown"]

// 50 last years
const years = Array(50).fill(0).map( (d,i) => new Date().getFullYear() - i )

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
      prevGame : Object.assign({}, this.state.game) // add a backup
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

    console.log(title);

    return (
      <div>
        {editButton}
        <h1>
          <EditableText
            type="input"
            defaultValue={title}
            fieldId="title"
            editing={editMode}
            handleChange={ d => {
              let game  = this.state.game
              game.title = d.text
              this.setState({ game });
              console.log(this.state.prevGame.title, this.state.game.title);
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
            defaultValue={description.summary}
            fieldId="description.summary"
            editing={editMode}
            handleChange={ d => {
              let game  = this.state.game
              game.description.summary = d.text
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
               defaultValue={source.url}
               fieldId="source.url"
               editing={editMode}
               handleChange={ d => {
                 let game  = this.state.game
                 game.source.url = d.text
                 this.setState({ game });
               }}
               />
              }
          <br/>
          Under license :
          <Selector
            editing={editMode}
            defaultValue={credentials.license}
            options={licenses}
            fieldId="credentials.license"
            handleChange={ d => {
              let game  = this.state.game
              game.credentials.license = d.value
              this.setState({ game });
            }}
          />
          <br/>
          Published in :
          <Selector
            editing={editMode}
            defaultValue={credentials.publication_year}
            options={years}
            fieldId="credentials.publication_year"
            handleChange={ d => {
              let game  = this.state.game
              game.credentials.publication_year = d.value
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
                defaultValue={audience.language}
                options={languages}
                handleChange={ d => {
                  let game  = this.state.game
                  game.audience.language = d.value
                  this.setState({ game });
                }}
              />

              <br/>
              Number_of_players:   {audience.number_of_players.players_min}-{audience.number_of_players.players_max}
              <br/>
            Duration of each play (minutes):
            <Number
              editing={editMode}
              defaultValue={audience.duration}
              fieldId="audience.duration"
              handleChange={ d => {
                let game  = this.state.game
                game.audience.duration = d.value
                this.setState({ game });
              }}
            />
            </p>
          </div>
          <div className="six columns">
            <MultiSelect
              defaultValue={audience.age}
              options={ages}
              editing={editMode}
              handleChange={ d => {
                let game  = this.state.game
                game.audience.age = d.items
                this.setState({ game });
              }}
            />
          </div>
        </div>

        <hr/>

        <div className="row">
          <div className="six columns">
            {/* <h5>Fabrication</h5> */}
            <p>
              Fab time (minutes):
              <Number
                editing={editMode}
                defaultValue={fabrication.fab_time}
                fieldId="fabrication.fab_time"
                handleChange={ d => {
                  let game  = this.state.game
                  game.fabrication.fab_time = d.value
                  this.setState({ game });
                }}
              />
            </p>
            <MultiSelect
              options={["ha"]}
              defaultValue={fabrication.requirements}
            />
          </div>
          <div className="six columns">
            <h5>Download files</h5>
            {/* <MultiSelect items={this.props.files}/> */}
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
                game.credentials.authors = d.items
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
                game.credentials.illustrators = d.items
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
                game.credentials.publishers = d.items
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
