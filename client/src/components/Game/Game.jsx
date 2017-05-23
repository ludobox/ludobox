import React from 'react'
import APIClient from "../../api.js"
import GameForm from "../GameForm/GameForm.jsx"

export default class Game extends React.Component {

  constructor(props) {
    super(props)
    this.api = new APIClient()
    this.state = {
      game: null,
      prevGame : null,
      files: [],
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
      <span>

        {editButton}

        <hr />

        { this.state.game && this.state.files ?
          <GameForm
            game={this.state.game}
            files={this.state.files}
            editMode={editMode}
            updateGame={game => this.updateGame(game)}
            errors={{}}
          />
          :
          null
        }
      </span>
    )
  }
}
