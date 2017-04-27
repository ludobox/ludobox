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
      downloadEvent: null
    };
  }

  componentDidMount() {
    this.props.socket.on("downloadEvent", message => {
      console.log("downloadEvent", message);
      if(message.slug === this.props.slug)
        this.setState({ downloadEvent : message.message })
    })
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
      <span style={{overflow:"hidden"}}>
        { this.state.downloading ?
          this.state.downloadEvent
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
