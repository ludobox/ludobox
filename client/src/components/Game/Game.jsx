import React from 'react'
import AlertContainer from 'react-alert'

import APIClient from "../../api.js"
import GameForm from "../GameForm/GameForm.jsx"
import History from "./History.jsx"

import validator from 'is-my-json-valid'
import model from '../../../../model/game.json'

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
      newFiles: [],
      errors: [],
      editMode : false
    };
  }

  handleAddFiles(files) {
    console.log(files);
    this.setState({newFiles : files });
  }

  handleDeleteFile(fileName) {

    // get slug
    let slug = document.location.pathname.split("/").pop()
    console.log(slug);

    this.api.deleteFile({ fileName, slug },
      resp => { // SUCCESS : File deleted
        console.log(resp.files);
        // show feedback
        this.msg.success( "Your file have been deleted.")

        const files = resp.files.map( f => ({
          url : this.api.getURL(`games/${slug}/files/${f}`),
          filename : f
        }))

        this.setState({editMode : false, files})
      },
      error => {
        console.log(error);
        this.msg.error( error.message )}
    )


  }

  handleFileUpload() {
    console.log(this.state.newFiles);

    if (!this.state.newFiles.length) {
      this.msg.error("No files. Please add a file to upload.")
      return
    }

    // get slug
    let slug = document.location.pathname.split("/").pop()
    console.log(slug);
    // send files to server
    this.api.postFiles(slug,
      this.state.newFiles,
      resp => { // SUCCESS : Game created
        console.log(resp.files);
        // show feedback
        this.msg.success( "Bravo, your files have been posted!")

        const files = resp.files.map( f => ({
          url : this.api.getURL(`games/${slug}/files/${f}`),
          filename : f
        }))

        this.setState({editMode : false, files})
      },
      error => {
        console.log(error);
        this.msg.error( error.message )}
    )
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

        { this.state.game && this.state.files ?
          <GameForm
            game={this.state.game}
            editMode={editMode}
            updateGame={game => this.updateGame(game)}
            errors={this.state.errors}
            files={this.state.files}
            newFiles={this.state.newFiles}
            handleAddFiles={ files => this.handleAddFiles(files)}
            handleDeleteFile={ file => this.handleDeleteFile(file)}
            handleFileUpload={ files => this.handleFileUpload(files)} // if defined, will add a upload button to push files directly
          />
          :
          null
        }


        <hr />

        <div className="row" style={{paddingBottom : '3em'}}>
          <div className="six columns">
            {editButton}
          </div>
          <div className="six columns">
            {
              this.state.game && this.state.game.history ?
              <History
                history={this.state.game.history}
              />
              :
              null
            }
          </div>
        </div>



        <AlertContainer ref={a => this.msg = a} {...this.alertOptions} />

      </span>
    )
  }
}
