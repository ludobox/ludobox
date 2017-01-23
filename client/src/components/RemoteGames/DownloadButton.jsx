import React from 'react'

import APIClient from "../../api.js"

export default class DownloadButton extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      downloading: false
    };
  }

  this.handleClick(gameSlug) {
    this.setState({ downloading : true })
    this.props.api.fetchGame(gameSlug,
      game => this.setState({ downloading : false }),
      game => this.setState({ downloading : false })
    )
  }

  render () {
    return (
      {
        this.state.downloading ?
          "Downloading..."
        :
          <a
            href="#"
            onClick={() => this.handleClick(gameSlug) }
            >
              "Download"
          </a>
      }
    )
  }
