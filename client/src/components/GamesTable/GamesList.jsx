import React from 'react';

import GamesListItem from './GamesListItem.jsx'

const GamesList = ({
  games,
  socket,
  remoteApi,
  localApi,
  isEditor
}) => (
  <div className='games-list'>
    <h5>There is currently {games.length} games you can fabricate.</h5>
    <table className="twelve columns" style={{tableLayout:"fixed"}}>
      <thead>
        <tr>
          <td>Title</td>
          <td>Language</td>
          <td>Gameplay</td>
          <td>Intention</td>
          <td>Status</td>
          {
            remoteApi ?
            <td>Download</td>
            :
            null
          }
          {
            isEditor ?
              <td>Edit</td>
            :
              null
          }
        </tr>
      </thead>
      <tbody>
        {
          games.map( game => (
            <GamesListItem
              key={game.slug}
              socket={socket}
              remoteApi={remoteApi}
              localApi={localApi}
              game={game}
              isEditor={isEditor}
              />
          ))
        }
      </tbody>
    </table>
  </div>
)



export default GamesList
