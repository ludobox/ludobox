import React from 'react';
import { FormattedMessage, defineMessages } from 'react-intl'

import GamesListItem from './GamesListItem.jsx'

const messages = defineMessages({
  count: {
    id: 'gamesList.count',
    defaultMessage: `There is currently {count} games you can fabricate.`
  },
  title: {
    id: 'gamesList.header.title',
    defaultMessage: `Title`
  },
  gameplay: {
    id: 'gamesList.header.gameplay',
    defaultMessage: `Gameplay`
  },
  intention: {
    id: 'gamesList.header.intention',
    defaultMessage: `Intention`
  },
  status: {
    id: 'gamesList.header.status',
    defaultMessage: `Status`
  }
})

const GamesList = ({
  games,
  socket,
  remoteApi,
  localApi,
  isEditor
}) => (
  <div className='games-list'>
    <h5>
      <FormattedMessage {...messages.count} values={{count : games.length}}/>
    </h5>
    <table className="twelve columns" >
      <thead>
        <tr>
          <td style={{width:"20%"}}>
            <FormattedMessage {...messages.title} />
          </td>
          {/* <td>Language</td> */}
          <td>
            <FormattedMessage {...messages.gameplay} />
          </td>
          <td>
            <FormattedMessage {...messages.intention} />
          </td>
          <td>
            <FormattedMessage {...messages.status} />
          </td>
          <td>{/*Fabricate*/}</td>
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
