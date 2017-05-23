import React from 'react'
import AlertContainer from 'react-alert'

import APIClient from "../../api.js"
import GameForm from "../GameForm/GameForm.jsx"

import validator from 'is-my-json-valid'
import model from '../../../../model/schema.json'

const alertOptions = {
  offset: 14,
  position: 'bottom left',
  theme: 'dark',
  time: 5000,
  transition: 'scale'
}

export default class Game extends React.Component {

  constructor(props) {
    super(props)
    this.api = new APIClient()
    this.validate = validator(model)
    this.state = {
      game: null,
      prevGame : null,
      files: [],
      errors: [],
      editMode : false
    };
  }

  fetchGame(slug) {
    this.api.getGame(slug, game => this.setState({ game }));
  }

  fetchFiles(slug) {
    this.api.getGameFilesList(slug, files => this.setState({ files }));
  }

  componentDidMount() {
    this.fetchGame(this.props.params.gameSlug)
    this.fetchFiles(this.props.params.gameSlug)
  }

  sendChanges() {

    // data validation
    this.validate(this.state.game);
    console.log(this.validate.errors);

    if (this.validate.errors) {
      this.msg.error(this.validate.errors.length + " errors.")

      const errors = {}
      this.validate.errors.map( error =>
        errors[error.field.slice(5)] = error.message
      )
      this.setState({ errors })
    } else {
      this.setState({errors : {}})

      // get slug
      let slug = document.location.pathname.split("/").pop()
      console.log(slug);
      // send changes to server
      this.api.updateGame(this.state.game,
        slug,
        resp => { // SUCCESS : Game created
          // show feedback
          this.msg.success( "Bravo, your game has been updated!")
        },
        error => this.msg.error( error.message )
      )

      // switch to read mode
      this.setState({
        editMode : false
      })
    }
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

  updateGame(game) {
    this.setState({game})
  }

  render() {

    let { editMode } = this.state

    // edit button
    let editButtonStyle = {
      fontSize:"10pt",
      cursor : "pointer"
    }

    let editButton = editMode ?
      <span>
        <a className="button"
          onClick={() => this.sendChanges()}
          style={editButtonStyle}
          >
          <i className="icono-check"></i>
        </a>
        <a className="button"
          onClick={() => this.cancelChanges()}
          style={editButtonStyle}
          >
          <i className="icono-cross"></i>
        </a>
      </span>
      :
      <a
        className="button"
        onClick={() => this.handleEditToggle()}
        style={editButtonStyle}
        >
        Edit
      </a>

    return (
      <span>

        {editButton}

        <hr />

        { this.state.game && this.state.files ?
          <GameForm
            game={this.state.game}
            files={this.state.files}
            editMode={editMode}
            updateGame={game => this.updateGame(game)}
            errors={this.state.errors}
          />
          :
          null
        }

        <AlertContainer ref={a => this.msg = a} {...this.alertOptions} />
      </span>
    )
  }
}
