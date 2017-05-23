import React from 'react'
import GameForm from "../GameForm/GameForm.jsx"

const emptyGame = {
  audience : {
    number_of_players : {}
  },
  credentials : {},
  description  : {},
  fabrication  : {},
  source  : {},
  title  : null,
  timestamp_add : null,
  content_type  : null,
}

export default class AddGame extends React.Component {

  constructor(props) {
    super(props)

    this.state = {
      game : emptyGame,
      files: [],
      editMode : true
    };
  }

  // onSubmit(resp){
  //   // TODO : validate data
  //   console.log("yay I'm valid!")
  //
  //   this.setState({ info : resp.formData })
  //   if( ! this.state.files.length)
  //     this.refs.container.error(
  //         "Please add a file...",
  //         "No files attached",
  //       {
  //         closeButton:true,
  //         handleOnClick: function() { console.log("click") }
  //       }
  //     )
  //   else {
  //     // POST
  //     console.log(`ok, let's post that info with ${this.state.files.length} files !`)
  //
  //     this.api.postGame(resp.formData,
  //       this.state.files,
  //       resp => { // SUCCESS : Game created
  //         // console.log(path);
  //         // show feedback
  //         this.refs.container.success(
  //             "Games stored ok!",
  //             "Bravo",
  //           {
  //             closeButton:true,
  //             handleOnClick: function() { console.log("click") }
  //           }
  //         )
  //         // go to page
  //         browserHistory.push('/games/'+resp.slug);
  //       },
  //       error => this.refs.container.error(
  //           error.message,
  //           null,
  //         {
  //           closeButton:true,
  //           handleOnClick: function() { console.log("click") }
  //         }
  //       )
  //     )
  //   }
  // }

  updateGame(game) {
    this.setState({game})
  }

  handleCreate() {
    console.log("create new game");
  }

  handleClearContent() {
    this.setState({ game : emptyGame })
  }

  render() {

    const {
      game,
      files,
      editMode
    } = this.state;

    // edit button
    let editButtonStyle = {
      cursor : "pointer",
      color : 'green'
    }

    return (
      <span>
        <GameForm
          game={game}
          files={files}
          editMode={editMode}
          updateGame={game => this.updateGame(game)}
        />
        <hr/>
        <a
          onClick={() => this.handleCreate()}
          style={editButtonStyle}
          >
          <i className="icono-check"></i>(CREATE NEW GAME)
        </a>
        <a
          onClick={() => this.handleClearContent()}
          style={editButtonStyle}
          >
          <i className="icono-trash"></i>(DELETE)
        </a>
        <br/>
      </span>
    )
  }
}
