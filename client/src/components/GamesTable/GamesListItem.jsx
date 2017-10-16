import React from 'react';

import ISO6391 from 'iso-639-1';

import DownloadButton from '../RemoteGames/DownloadButton.jsx';
import ContentState from '../ContentState/ContentState.jsx';

const GamesListItem = ({
  isEditor,
  socket,
  remoteApi,
  localApi,
  game
}) => (
  <tr style={ game.existsLocally ? { background : "yellow" } : {}  }>
    <td>
      <a href={"/games/"+game.slug}
        title={game.description.summary}
        >
        {game.title}
      </a>
    </td>
    {/* <td>
      {
        game.audience ?
          ISO6391.getName(game.audience.language)  //
        : null
      }
    </td> */}
    <td>
      {game.description.gameplay}
    </td>
    <td>
      {game.description.intention}
    </td>
    <td>
      <a style={{textDecoration: "none"}}
        href={"/games/"+game.slug}>
          <ContentState state={game.state} errors={game.errors} />
      </a>
    </td>
    <td>
      <a className="button button-primary" href={"/games/"+game.slug}>
          Print & Play
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
    {
      isEditor ?
        <td className="edit-button">
          <a href={`/games/${game.slug}/edit`}>&#9997;</a>
        </td>
      :
        null
    }
  </tr>
)
export default GamesListItem
