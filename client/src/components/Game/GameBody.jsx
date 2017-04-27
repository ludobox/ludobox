import React from 'react'

import EditableText from '../Form/EditableText.jsx'

class SmallList extends React.Component {
  constructor(props) { super(props) }
  render() {
    const styleLi = {
      // display : "inline",
      padding : "0 .5em",
      margin : ".5em ",
      width: "auto",
      lineHeight: "2.5em",
      display: "inline-block",
      border : "1px solid #ccc"
    },
    styleUl = { listStyle : "none"}

    const lis = this.props.items.map( (item, i) =>
      <li key={i} style={styleLi}>{item}</li>
    )

    return (
      <ul style={styleUl}>
        {lis}
      </ul>
    )
  }
}

export default class GameBody extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      game : this.props.game
    }
    this.updateGameData = this.updateGameData.bind(this)
  }

  updateGameData(dataChange) {
    console.log(dataChange);
    const id = dataChange.id.split(".")
    let update = {}
    switch (id.length) {
      case 1 :
        update[dataChange.id] = dataChange.text
        console.log(update);
        this.setState({ game : Object.assign(this.state.game, update) })
        break;
      // case 2 :
      //   update[id[0]] = {}
      //   update[id[0]][id[1]] = dataChange.text
      //   console.log(update);
      //   this.setState({ game : Object.assign(this.state.game, update) })
      //   break;
      default:
        console.log("ok")
    }
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

    return (
      <div>
        <h1>
          <EditableText
            type="input"
            defaultValue={title}
            fieldId="title"
            saveChanges={this.updateGameData}
            />
        </h1>

        <SmallList items={ description.themes.concat(description.genres)}/>
          <EditableText
            type="textarea"
            defaultValue={description.summary}
            fieldId="description.summary"
            saveChanges={this.updateGameData}
            />
        <p>
          Webpage: <a href="{source.url}" target="_blank">{source.url}</a>
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
