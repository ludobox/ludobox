import React from 'react'

import EditableText from '../Form/EditableText.jsx'
import FreeTagging from '../Form/FreeTagging.jsx'
import MultiSelect from '../Form/MultiSelect.jsx'
import Selector from '../Form/Selector.jsx'
import Number from '../Form/Number.jsx'
import FilesList from '../Form/FilesList.jsx'

import ISO6391 from 'iso-639-1'

import ContentState from '../ContentState/ContentState.jsx'
import model from '../../../../model/game.json'

const requirements = model.properties.fabrication.properties.requirements.items.enum
  .map(d => ({ value : d, name: d }))

const licenses = model.properties.credentials.properties.license.enum
  .map(d => ({name : d, value : d}))

const intentions = model.properties.description.properties.intention.enum
  .map(d => ({name : d, value : d}))

const gameplays = model.properties.description.properties.gameplay.enum
  .map(d => ({name : d, value : d}))

const gametypes = model.properties.description.properties.type.enum
  .map(d => ({name : d, value : d}))

const mechanics = model.properties.description.properties.mechanics.items.enum
  .map(d => ({name : d, value : d}))

const ages = model.properties.audience.properties.age.items.enum
  .map(d => ({name : d, value : d}))

// 50 last years
const years = [
  ...Array(50)
    .fill(0)
    .map( (d,i) => {
      let y = new Date().getFullYear() - i
      return { name : y, value : y }
    } )
]

// languages code
const languages = ISO6391.getLanguages(ISO6391.getAllCodes())
    .map(d => ({ name : d.name, value : d.code}))

export default class GameForm extends React.Component {

  updateGame(game) {
    this.props.updateGame(game)
  }

  render() {
    const {
      audience,
      credentials,
      description,
      fabrication,
      source,
      state,
      timestamp_add,
      title,
      content_type
    } = this.props.game

    const {
      editMode,
      errors,
      maxFileSize
    } = this.props

    // TODO : make title editable
    return (
      <div>
        <h1>
          <EditableText
            type="input"
            text={title}
            error={errors["title"]}
            editing={editMode}
            placeholder="Add a title..."
            handleChange={ d => {
              let game  = this.props.game
              game.title = d
              this.updateGame( game );
            }}
            />
        </h1>
        { ! editMode ?
          <p>
            <ContentState
              state={state}
              errors={this.props.game.errors}
            />
          </p>
          :
          null
        }
        <EditableText
          type="textarea"
          text={description.summary}
          placeholder="Add a description..."
          error={errors["description.summary"]}
          editing={editMode}
          handleChange={ d => {
            let game  = this.props.game
            game.description.summary = d
            this.updateGame( game );
          }}
          />
        <p>
            <span className="label">Webpage</span>
            { !editMode ?
              <a href={source.url} target="_blank">
                {source.url}
              </a>
              :
              <EditableText
               type="input"
               text={source.url}
               error={errors["source.url"]}
               fieldType="url"
               editing={editMode}
               handleChange={ d => {
                 let game  = this.props.game
                 game.source.url = d
                 this.updateGame( game );
               }}
               />
              }
          <br/>
          <span className="label">Under license </span>
          <Selector
            editing={editMode}
            value={credentials.license}
            error={errors["credentials.license"]}
            options={licenses}
            handleChange={ d => {
              let game  = this.props.game
              game.credentials.license = d
              this.updateGame( game );
            }}
          />
          <br/>
          <span className="label">Published in </span>
          <Selector
            editing={editMode}
            value={credentials.publication_year}
            error={errors["credentials.publication_year"]}
            options={years}
            handleChange={ d => {
              let game  = this.props.game
              let year = parseInt(d)
              game.credentials.publication_year = year
              this.updateGame( game );
            }}
          />
        </p>
        <hr/>
        <p>
          <br/>
          <span className="label">Intention</span>
          <Selector
            editing={editMode}
            value={description.intention}
            error={errors["description.intention"]}
            options={intentions}
            handleChange={ d => {
              let game  = this.props.game
              game.description.intention = d
              this.updateGame( game );
            }}
          />
          <br/>
          <span className="label">Gameplay</span>
          <Selector
            editing={editMode}
            value={description.gameplay}
            error={errors["description.gameplay"]}
            options={gameplays}
            handleChange={ d => {
              let game  = this.props.game
              game.description.gameplay = d
              this.updateGame( game );
            }}
          />
          <br />
          <span className="label">Type</span>
          <Selector
            editing={editMode}
            value={description.type}
            error={errors["description.type"]}
            options={gametypes}
            handleChange={ d => {
              let game  = this.props.game
              game.description.type = d
              this.updateGame( game );
            }}
          />
          <br />
          <span className="label">Mechanics</span>
          <MultiSelect
            editing={editMode}
            value={description.mechanics}
            error={errors["description.mechanics"]}
            options={mechanics}
            handleChange={ d => {
              let game  = this.props.game
              game.description.mechanics = d
              this.updateGame( game );
            }}
          />
          <br />
          <span className="label">Tags</span>
          <FreeTagging
            items={description.tags}
            editing={editMode}
            error={errors["description.tags"]}
            handleChange={ d => {
              let game  = this.props.game
              game.description.tags = d
              this.updateGame( game );
            }}
          />
        </p>
        <hr/>
        <div className="row">
          <div className="six columns">
            <p>
              <span className="label">Language</span>
              <Selector
                editing={editMode}
                value={audience.language}
                error={errors["audience.language"]}
                options={languages}
                handleChange={ d => {
                  let game  = this.props.game
                  game.audience.language = d
                  this.updateGame( game );
                }}
              />

              <br/>
              <span className="label">
                Number of players :
                { editMode ? " (minimum)" : null}
              </span>
              <Number
                editing={editMode}
                value={audience.number_of_players.players_min}
                error={errors["audience.number_of_players.players_min"]}
                handleChange={ d => {
                  let game  = this.props.game
                  game.audience.number_of_players.players_min = d
                  this.updateGame( game );
                }}
              />

                { editMode ?
                  <span className="label">
                      Number of players (maximum)
                  </span>
                 : null
               }
              <Number
                editing={editMode}
                value={audience.number_of_players.players_max}
                error={errors["audience.number_of_players.players_max"]}
                handleChange={ d => {
                  let game  = this.props.game
                  game.audience.number_of_players.players_max = d
                  this.updateGame( game );
                }}
              />
              <br/>
            <span className="label">Duration of each play (minutes):</span>
            <Number
              editing={editMode}
              value={audience.duration}
              error={errors["audience.duration"]}
              handleChange={ d => {
                let game  = this.props.game
                game.audience.duration = d
                this.updateGame( game );
              }}
            />
            </p>
          </div>
          <div className="six columns">
            {
              editMode ?
                <span className="label">
                  Audience Age
                </span>
              :
              null
            }
            <MultiSelect
              value={audience.age}
              error={errors["audience.age"]}
              options={ages}
              editing={editMode}
              handleChange={ d => {
                let game  = this.props.game
                game.audience.age = d
                this.updateGame( game );
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
                <span className="label">
                  Fabrication time (minutes)
                </span>
                <Number
                  editing={editMode}
                  error={errors["fabrication.fab_time"]}
                  value={fabrication.fab_time}
                  fieldId="fabrication.fab_time"
                  handleChange={ d => {
                    let game  = this.props.game
                    game.fabrication.fab_time = d
                    this.updateGame( game );
                  }}
              />
              </p>
            }
            <h5>Requirements</h5>
            <MultiSelect
              value={fabrication.requirements}
              error={errors["fabrication.requirements"]}
              options={requirements}
              editing={editMode}
              handleChange={ d => {
                let game  = this.props.game
                game.fabrication.requirements = d
                this.updateGame( game );
              }}
            />
          </div>
          <div className="six columns">
            <h5>Download files</h5>
            <FilesList
              files={this.props.files}
              newFiles={this.props.newFiles}
              editing={editMode}
              handleFileUpload={this.props.handleFileUpload }
              handleDeleteFile={this.props.handleDeleteFile }
              handleAddFiles={ files => this.props.handleAddFiles(files) }
              maxFileSize={maxFileSize}
            />
          </div>
        </div>

        <hr/>

        <div className="row">
          <div className="four columns">
            <p className="label">Authors</p>
            <FreeTagging
              items={credentials.authors}
              editing={editMode}
              error={errors["credentials.authors"]}
              handleChange={ d => {
                let game  = this.props.game
                game.credentials.authors = d
                this.updateGame( game );
              }}
            />
          </div>
          <div className="four columns">
            <p className="label">Illustrators</p>
            <FreeTagging
              items={credentials.illustrators}
              error={errors["credentials.illustrators"]}
              editing={editMode}
              handleChange={ d => {
                let game  = this.props.game
                game.credentials.illustrators = d
                this.updateGame( game );
              }}
            />
          </div>
          <div className="four columns">
            <p className="label">Publishers</p>
            <FreeTagging
              items={credentials.publishers}
              error={errors["credentials.publishers"]}
              editing={editMode}
              handleChange={ d => {
                let game  = this.props.game
                game.credentials.publishers = d
                this.updateGame( game );
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
