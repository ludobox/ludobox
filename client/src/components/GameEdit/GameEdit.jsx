import React from 'react'
import {browserHistory} from 'react-router'
import AlertContainer from 'react-alert'

import APIClient from "../../api.js"
import GameForm from "../GameForm/GameForm.jsx"
import ActionButtons from "../ActionButtons/ActionButtons.jsx"
import History from "../History/History.jsx"

import validator from 'is-my-json-valid'
import model from '../../../../model/game.json'

const alertOptions = {
  offset: 14,
  position: 'bottom left',
  theme: 'dark',
  time: 5000,
  transition: 'scale'
}

// edit button
let editButtonStyle = {
  fontSize:"10pt",
  cursor : "pointer"
}

export default class GameEdit extends React.Component {

  constructor(props) {
    super(props)
    this.api = new APIClient()
    this.validate = validator(model)
    this.state = {
      game: null,
      // prevGame : JSON.parse(JSON.stringify(this.state.game)),
      prevGame : null,
      files: [],
      newFiles: [],
      errors: [],
      editMode : false
    };
  }

  fetchGame(slug) {
    this.api.getGame(slug, game => {
      let { files } = game
      files = files.map( f => ({
        url : this.api.getURL(`games/${slug}/files/${f}`),
        filename : f
      }))
      this.setState({ game, files })
    });
  }

  componentDidMount() {
    this.fetchGame(this.props.params.gameSlug)
  }

  handleAddFiles(files) {
    console.log(files);
    this.setState({newFiles : files });
  }

  handleDeleteFile(fileName) {

    // get slug
    let slug = this.state.game.slug
    console.log(slug);

    this.api.deleteFile(slug, fileName,
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
    let slug = this.state.game.slug

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
      let slug = this.state.game.slug

      // send changes to server
      this.api.updateGame(this.state.game,
        slug,
        resp => { // SUCCESS : Game created
          // show feedback
          this.msg.success( "Bravo, your game has been updated!")
        },
        error => this.msg.error( error.message )
      )

      // Move to /games/switch to read mode
      browserHistory.push(`/games/${slug}`)
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

  handleSendChanges() {
    this.updateGameData()
  }

  updateGame(game) {
    this.setState({game})
  }

  render() {
    return (
      <div>
      {
        this.state.game && this.state.files ?
        <GameForm
          game={this.state.game}
          editMode={true}
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
      <AlertContainer ref={a => this.msg = a} {...this.alertOptions} />
    </div>
    )
  }

}
