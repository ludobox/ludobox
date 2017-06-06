import React from 'react'

import EditableText from '../Form/EditableText.jsx'
import FreeTagging from '../Form/FreeTagging.jsx'
import MultiSelect from '../Form/MultiSelect.jsx'
import Selector from '../Form/Selector.jsx'
import Number from '../Form/Number.jsx'
import FilesList from '../Form/FilesList.jsx'
import ThumbnailForm from '../Form/ThumbnailForm.jsx'

import ISO6391 from 'iso-639-1'

const licenses = [null, "CC0", "CC BY-NC-SA 4.0", "Public Domain", "No License", "Unknown"]

const years = [null, ...Array(50).fill(0).map( (d,i) => new Date().getFullYear() - i )] // 50 last years

const ages = ["Children", "Teenagers", "Adults"]
const languages = [null, ...ISO6391.getAllCodes()]

export default class GameForm extends React.Component {

  updateGame(game) {
    this.props.updateGame(game)
  }

  render() {
    const {
      audience,
      credentials,
      description ,
      fabrication ,
      source ,
      timestamp_add,
      title ,
      content_type ,
    } = this.props.game

    const { editMode, errors } = this.props
    
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

        <ThumbnailForm
          handleFileUpload={this.props.handleFileUpload}
          />

          {/*
            // TODO : themes and genres
            <FreeTagging
            items={ description.themes.concat(description.genres)}
            editing={editMode}
            handleChange={ d => {
              let game  = this.props.game
              game.description.themes = d.items
              this.updateGame( game );
            }}
          /> */}

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
            Webpage:
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
          Under license :
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
          Published in :
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

        <div className="row">
          <div className="six columns">
            <p>
              Language:
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
              Number of players :
              { editMode ? " (minimum)" : null}
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
               -
              { editMode ? "Number_of_players (maximum)" : null}
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
            Duration of each play (minutes):
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
            {editMode ? "Audience Age" : null}
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
                Fabrication time (minutes):
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
            <MultiSelect
              options={["ha"]}
              value={fabrication.requirements}
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
            />
          </div>
        </div>

        <hr/>

        <div className="row">
          <div className="four columns">
            <p>Authors</p>
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
            <p>Illustrators</p>
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
            <p>Publishers</p>
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
