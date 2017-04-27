import React from 'react'

class SmallList extends React.Component {
  constructor(props) { super(props) }
  render() {
    const styleLi = {
      display : "inline",
      padding : ".5em",
      margin : "0 0.5em",
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
  }

  render() {
    // console.log(this.props.game);

    const audience = this.props.game.audience,
      credentials = this.props.game.credentials,
      description = this.props.game.description,
      fabrication = this.props.game.fabrication,
      source = this.props.game.source,
      timestamp_add = this.props.game.timestamp_add,
      title = this.props.game.title,
      content_type = this.props.game.content_type;

    return (
      <div>
        <h1>{title}</h1>
        <SmallList items={ description.themes.concat(description.genres)}/>
        <p>{description.summary}</p>
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
