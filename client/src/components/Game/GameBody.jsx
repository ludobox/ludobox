import React from 'react'

import EditableText from '../Form/EditableText.jsx'
import SmallList from '../Form/SmallList.jsx'

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

  handleChange(dataChange) {
    console.log(dataChange);
    console.log(this);
    // 'a.b.etc'.split('.').reduce((o,i)=>o[i], obj)
    // this.setState({ text:  })
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

        <SmallList items={ description.themes.concat(description.genres)}/>
          <EditableText
            type="textarea"
            defaultValue={description.summary}
            fieldId="description.summary"
            editing={editMode}
            handleChange={this.handleChange}
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
               handleChange={this.handleChange}
               />
              }
          <br/>
          Published in {credentials.publication_year} under license : {credentials.license}
        </p>
        <hr/>

        <div className="row">
          <div className="six columns">
            <p>
              Language:  {audience.language}
              <br/>
              Number_of_players:   {audience.number_of_players.players_min}-{audience.number_of_players.players_max}
              <br/>
            Duration of each play: {audience.duration} min</p>
          </div>
          <div className="six columns">
            <SmallList items={audience.age}/>
          </div>
        </div>

        <hr/>

        <div className="row">
          <div className="six columns">
            {/* <h5>Fabrication</h5> */}
            <p>Fab time: {fabrication.fab_time} min</p>
            <SmallList items={fabrication.requirements}/>
          </div>
          <div className="six columns">
            <h5>Download files</h5>
            <SmallList items={this.props.files}/>
          </div>
        </div>

        <hr/>

        <div className="row">
          <div className="four columns">
            <p>Authors</p>
            <SmallList items={credentials.authors}/>
          </div>
          <div className="four columns">
            <p>Illustrators</p>
            <SmallList items={credentials.illustrators}/>
          </div>
          <div className="four columns">
            <p>Publishers</p>
            <SmallList items={credentials.publishers}/>
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
