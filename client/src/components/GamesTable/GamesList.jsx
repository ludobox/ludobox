import React from 'react';

import ISO6391 from 'iso-639-1';

import DownloadButton from '../RemoteGames/DownloadButton.jsx';
import ContentState from '../ContentState/ContentState.jsx';

const GamesList = ({games, socket, remoteApi, localApi}) => (
  <div>
    <p><small>{games.length} Games</small>  </p>
    <table className="twelve columns" style={{tableLayout:"fixed"}}>
      <thead>
        <tr>
          <td>Title</td>
          {/* <td>Fab Time</td> */}
          <td>Language</td>
          <td>Status</td>
          {
            remoteApi ?
            <td>Download</td>
            :
            null
          }
        </tr>
      </thead>
      <tbody>
        {
          games.map( game => (
            <tr style={ game.existsLocally ? { background : "yellow" } : {}  }
              key={game.slug}>
              <td>
                <a href={"/games/"+game.slug}
                  title={game.description.summary}
                  >
                  {game.title}
                </a>
              </td>

              <td>{
                game.audience ?
                  ISO6391.getName(game.audience.language)  //
                  : null
                }
              </td>
              <td>
                <a style={{textDecoration: "none"}}
                  href={"/games/"+game.slug}>
                    <ContentState state={game.state} errors={game.errors} />
                </a>
              </td>
              {
                ! game.existsLocally && remoteApi && localApi ?
                <td>
                  <DownloadButton
                    socket={socket}
                    remoteApi={remoteApi}
                    localApi={localApi}
                    slug={game.slug}
                    />
                </td>
                :
                null
              }
            </tr>
          ))
        }
      </tbody>
    </table>
  </div>
)



export default GamesList
