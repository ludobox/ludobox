import React from 'react'

export default class GamesTable extends React.Component {

  render() {
    let rows = this.props.games.map( game => (
      <tr style={ game.existsLocally ? { background : "yellow" } : {}  }
        key={game.slug}>
        <td>
          <a
            href={"/games/"+game.slug}
            // target="_blank"
            >
            {game.title}
          </a>
        </td>
        <td>{game.type}</td>
        <td>{game.fab_time}</td>
        <td>{game.language}</td>
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
