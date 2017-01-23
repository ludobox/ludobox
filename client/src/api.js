import axios from 'axios'

export default class APIClient {

  constructor(options={}) {
    console.log("init",  options);
    this.baseUrl = options.baseUrl;
  }

  handleError(error, errorCallback) {
    console.log("ERROR : " + error)
    if (errorCallback) errorCallback(error)
    else throw error
  }

  get(url, callback, errorCallback) {
    console.log("GET : " + url)
    axios.get(url)
      .then(res => {
        var info = res.data
        callback(info);
      })
      .catch((error) => {
        this.handleError(error, errorCallback)
      })
  }

  getURL(path) {
    return this.baseUrl ? `${this.baseUrl}/api/${path}` : `/api/${path}`
  }

  getGame(slug) {
    let gameUrl = this.getURL(`games/${slug}/info.json`);
    this.get(gameUrl, info => console.log(info.title))
  }

  getGameFilesList(slug) {
    let gameUrl = this.getURL(`files/${slug}/info.json`);
    this.get(gameUrl, files => console.log(files))
  }

  getGames(callback) {
    let gamesUrl = this.getURL(`games`);
    this.get(gamesUrl, gamesList => callback(gamesList))
  }

}
