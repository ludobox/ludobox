import React from 'react'

export default class DownloadButton extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      downloading: false,
      game : {},
      gameReady: false,
      files : [],
      filesReady : false,
      downloadEnded: false
    };
  }

  // TODO fix callback spagheti
  handleClick(gameSlug) {
    this.setState({ downloading : true })

    // get the game
    this.props.remoteApi.getGame(gameSlug, game => {
      this.setState({ game })
      this.setState({ gameReady : true })
      // download files list
      this.props.remoteApi.getGameFilesList(gameSlug, files => {
        this.setState({ files })
        this.setState({ filesReady : true })
        let opts = {
            info : this.state.game,
            files : files,
            slug : gameSlug
          }
          this.props.localApi.cloneGame( opts, clonedGame => {
            console.log(clonedGame, "game cloned.");
        })
      })
    })
  }

  render () {

    return (
      <span>
        { this.state.downloading ?
          "Downloading..."
          :
            this.state.downloadEnded ?
            null
            :
            <a
              href="#"
              onClick={() => this.handleClick(this.props.slug) }
              >
              Download
            </a>
        }
      </span>
    )
  }
}
