import React from 'react'

export default class GamesTable extends React.Component {

  handleClick(slug){
    this.props.fetchGame(slug)
  }

  render() {
    let rows = this.props.games.map( game => (
      <tr style={ game.existsLocally ? { background : "yellow" } : {}  }
        key={game.slug}>
        <td>
          <a
            href={
              !game.existsLocally ?
                this.props.url+"/games/"+game.slug
                :
                "/games/"+game.slug
            }
            target="_blank"
            >
            {game.title}
          </a>
        </td>
        <td>{game.type}</td>
        <td>{game.fab_time}</td>
        <td>{game.language}</td>
        { ! game.existsLocally && this.props.url ?
          <td>
            <a
              href="#"
              onClick={() => this.handleClick(game.slug) }
              >
              {this.props.downloading.indexOf(game.slug) === -1 ?
                "Download"
                :
                "Downloading..."
              }
            </a>
          </td>
          :
          null
        }
      </tr>
    ))

    return (
      <div>
        <table className="twelve columns">
            <thead>
                <tr>
                    <td>Title</td>
                    <td>Type</td>
                    <td>fab_time</td>
                    <td>languages</td>
                </tr>
            </thead>
            <tbody>
              {rows}
            </tbody>
        </table>
      </div>
    )
  }
}
