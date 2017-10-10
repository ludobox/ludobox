import React from 'react'
import validator from 'is-my-json-valid'
import AlertContainer from 'react-alert'

import { browserHistory } from 'react-router'

import GameForm from "../GameForm/GameForm.jsx"
import APIClient from "../../api.js"
import model from '../../../../model/game.json'

const emptyGame = {
  audience : {
    number_of_players : {}
  },
  credentials : {},
  description  : {},
  fabrication  : {
    fab_time : 0
  },
  source  : {},
  title  : null,
  timestamp_add : String(new Date()),
  content_type  : "game",
}

const alertOptions = {
  offset: 14,
  position: 'bottom left',
  theme: 'dark',
  time: 5000,
  transition: 'scale'
}

export default class AddGame extends React.Component {

  constructor(props) {
    super(props)
    this.api = new APIClient()
    this.validate = validator(model)
    this.state = {
      game : emptyGame,
      newFiles: [],
      files: [],
      editMode : true,
      errors: {}
    };
  }

  handleAddFiles(files) {
    console.log(files);
    this.setState({newFiles : files });
  }

  postGame(formData) {
    this.api.postGame(this.state.game,
      this.state.newFiles,
      resp => { // SUCCESS : Game created
        console.log(resp);
        // show feedback
        this.msg.success( "Bravo, your games has been created!")
        // go to page
        browserHistory.push('/games/'+resp.slug);
      },
      error => this.msg.error( error.message )
    )
  }

  updateGame(game) {
    this.setState({game})
  }

  handleSubmit(e) {
    e.preventDefault()

    // data validation
    this.validate(this.state.game);

    if (this.validate.errors) {
      this.msg.error(this.validate.errors.length + " errors.")

      const errors = {}
      this.validate.errors.map( error =>
        errors[error.field.slice(5)] = error.message
      )
      this.setState({ errors })
    } else {
      this.setState({errors : {}})

      // check if files has been attached
      if( ! this.state.newFiles.length) {
        this.msg.error("No files attached, Please add a file...")
      } else {
        this.postGame()
      }
    }
  }

  render() {

    const {
      game,
      newFiles,
      editMode,
      errors
    } = this.state;

    // edit button
    let editButtonStyle = {
      cursor : "pointer",
      color : 'green'
    }

    return (
      <form
        onSubmit={ e => this.handleSubmit(e)}
        className="addGame"
        >
        <AlertContainer ref={a => this.msg = a} {...this.alertOptions} />
        <GameForm
          game={game}
          editMode={editMode}
          updateGame={game => this.updateGame(game)}
          errors={errors}
          files={[]} //no files
          newFiles={newFiles}
          handleAddFiles={ files => this.handleAddFiles(files)}
          handleFileUpload={null}
        />
        <hr/>
        <input
          type="submit"
          className="btn btn-primary"
          // onClick={e => e.preventDefault()}
          value="Create new Game"
          />
        <br/>
      </form>
    )
  }
}
