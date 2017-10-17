import React from 'react'
import {browserHistory} from 'react-router'
import AlertContainer from 'react-alert'

import PageTitle from '../PageTitle/PageTitle.jsx'

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
    this.setState({newFiles : files });
  }

  handleDeleteFile(fileName) {

    // get slug
    let {slug} = this.state.game

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

        this.setState({
          editMode : false,
          files,
          newFiles: []
        })
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

      const errors = {}
      let errorMsg = ""
      this.validate.errors.map( error => {

        let fieldName = error.field.split(".").length == 4 ?
          error.field.split(".").slice(1, -1).join(".") // handle multiselect errors
          :
          error.field.slice(5)

        errorMsg += `${fieldName} \n`
        return errors[fieldName] = error.message
      })

      this.msg.error(`${this.validate.errors.length} errors.\n\n ${errorMsg} `)

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
          // Move to /games/switch to read mode
          browserHistory.push(`/games/${slug}`)
        },
        error => this.msg.error( error.message )
      )

    }
  }

  cancelChanges() {
    let {slug} = this.state.game
    browserHistory.push(`/games/${slug}`)
  }

  handleSendChanges() {
    this.updateGameData()
  }

  updateGame(game) {
    this.setState({game})
  }

  render() {
    const {max_file_size} = this.props.config.config

    return (
      <div>
        <PageTitle title="Edit Game" />
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
          maxFileSize={max_file_size}
        />
        :
        null
      }
      <span>
       <a className="button"
         onClick={() => this.sendChanges()}
         style={editButtonStyle}
         >
           Update
       </a>
       <a className="button"
         onClick={() => this.cancelChanges()}
         style={editButtonStyle}
         >
           Cancel

       </a>
     </span>
      <AlertContainer
        ref={a => this.msg = a}
        {...this.alertOptions}
        />
    </div>
    )
  }

}
