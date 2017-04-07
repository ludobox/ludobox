import React from 'react'

export default class DownloadButton extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      downloading: false,
      game : {},
      gameReady: false,
      files : [],
      filesReady : false
    };
  }

  // TODO fix callback spagheti
  handleClick(gameSlug) {
    this.setState({ downloading : true })

    // get the game
    this.props.remoteApi.getGame(gameSlug, game => {
      this.setState({ game })
      this.setState({ gameReady : true })
      // donwload files list
      this.props.remoteApi.getGameFilesList(gameSlug, files => {
        this.setState({ files })
        this.setState({ filesReady : true })
        let opts = {
            info : this.state.game,
            files : files,
            slug : gameSlug
          }
        console.log(opts);
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
