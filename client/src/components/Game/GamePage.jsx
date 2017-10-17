import React from 'react'
import ISO6391 from 'iso-639-1'
import FileIcons from 'file-icons-js'
import 'file-icons-js/css/style.css'

import Markdown from 'react-remarkable'

import ActionButtons from "../ActionButtons/ActionButtons.jsx"
import PageTitle from '../PageTitle/PageTitle.jsx'
import History from "../History/History.jsx"

import './GamePage.scss'

const mapToList = (arr, sep=' - ') =>
  arr
    .filter(a => typeof a != 'undefined')
    .map((a,i,x) => i === x.length-1 ? a : a+ sep)


const parseHeader = (audience) => {
  const {duration, language, number_of_players} = audience
  const {players_min, players_max} = number_of_players

  const header = []

  const players = []
  if(players_min) players.push(players_min)
  if(players_max) players.push(players_max)
  if (players.length) header.push(`${mapToList(players, '-')} players`)

  if(duration) header.push(`${audience.duration} minutes`)

  if(language) header.push(ISO6391.getName(language))

  return mapToList(header, ' | ')
}

const GamePage = ({
  title,
  description,
  source,
  audience,
  fabrication,
  credentials,
  slug,
  history,
  contentState,
  files,
  user
}) => (
  <div className="single-game">

    <PageTitle
      title={title}
      subtitle={
        <span>
          {parseHeader(audience)}
          <br />
          {audience.age ? mapToList(audience.age) : null}
        </span>
    }
    />

    <Markdown>
      {description.summary}
    </Markdown>

    <div className="row">
      <div className="four columns">

      </div>
      <div className="eight columns">
      </div>
    </div>


    <div className="row">

      <div className="six columns infobox">

        <p>
          {mapToList([description.intention, description.gameplay, description.type])}
          {
            description.mechanics ?
              ' - '+ mapToList(description.mechanics)
            :
              null
          }
        </p>

        <ul className="credentials">
          {
            credentials.authors || credentials.illustrators || credentials.publishers ?
              <li><b>Credentials</b></li>
            :
            null
          }
          {
            credentials.authors ?
              <li>
                <span>Author(s):</span> {mapToList(credentials.authors, ', ')}
              </li>
            :
              null
          }
          {
            credentials.illustrators ?
              <li>
                <span>Illustrator(s):</span> {mapToList(credentials.illustrators, ', ')}
              </li>
            :
              null
          }
          {
            credentials.publishers ?
              <li>
                <span>Publisher(s):</span> {mapToList(credentials.publishers, ', ')}
              </li>
            :
              null
          }
        </ul>

        <p className="license">
          {credentials.license} {credentials.publication_year ? `(${credentials.publication_year})` : null}
        </p>

        <p className="weblink">
          <a
            href={source.url}
            target="_blank"
            title={source.url}
            >
            Source
          </a>
        </p>
      </div>

      <div className="six columns infobox">
        <h5>Fabrication time : {fabrication.fab_time} minutes </h5>

        {
          fabrication.requirements || fabrication.components ?
            <ul className="requirements">
              <li><b>What you need</b></li>
              {
                fabrication.requirements ?
                  fabrication.requirements.map(req =>
                    <li key={req}>&#10004; {req}</li>
                  )
                :
                null
              }
              {
                fabrication.components ?
                  fabrication.components.map(req =>
                    <li key={req}>&#9678; {req}</li>
                  )
                :
                  null
              }
            </ul>
          :
            null
        }

        <ul className="files">
          <li><b>Download Files</b></li>
          {
            files.map(f =>
              <li key={f.url}>
                <a
                  title={f.filename}
                  href={f.url}
                  >
                    <span className={'icon '+FileIcons.getClassWithColor(f.url)}></span>
                    {f.filename}
                </a>
              </li>
            )
          }
        </ul>
      </div>
    </div>

    <hr/>
    {
      description.tags ?
        <p className="tags-list"><b>Tags</b>  {mapToList(description.tags, ', ')}</p>
        :
        null
    }

    <History
      history={history}
      />
    <ActionButtons
      slug={slug}
      author={history[0].user}
      state={contentState}
      user={user}
      updateContent={() => this.updateContent()}
      />
  </div>
)

export default GamePage
