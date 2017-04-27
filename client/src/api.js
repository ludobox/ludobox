import axios from 'axios'

export default class APIClient {

  constructor(options={}) {
    console.log("init",  options);
    this.baseUrl = options.baseUrl;
  }

  handleError(error, errorCallback) {
    // console.log("ERROR : " + error)
    if (errorCallback && error.response) errorCallback(error.response.data)
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

  post(url, payload, callback, errorCallback) {
    console.log("POST : " + url)
    axios.post(url, payload)
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


  // APIpublic methods

  getInfo(callback) {
    let infoUrl = `/api`;
    console.log(infoUrl)
    this.get(infoUrl, info => callback(info))
  }

  getGame(slug, callback) {
    let gameUrl = this.getURL(`games/${slug}/info.json`);
    this.get(gameUrl, game => callback(game))
  }

  getGameFilesList(slug, callback) {
    let gameUrl = this.getURL(`files/${slug}`);

    this.get(gameUrl, files =>
      callback(files.map( f => (
        {
          url : this.getURL(`games/${slug}/files/${f}`),
          filename : f
        }
      )))
    )
  }

  cloneGame(opts, callback) {
    console.log(opts);
    let gameUrl = this.getURL(`clone`);
    this.post(gameUrl, opts, path => callback(path))
  }

  postGame(info, files, callback, callbackError) {
    console.log(info, files);
    let gameUrl = this.getURL(`create`);

    // create payload
    const payload = new FormData();
    // add files
    files.forEach( file =>
      payload.append('files', file, file.name)
    )
    // add info
    payload.append("info", JSON.stringify(info));

    // POST !
    this.post(gameUrl,
      payload,
      path => callback(path),
      error => callbackError(error)
    )
  }

  getGames(callback) {
    let gamesUrl = this.getURL(`games`);
    this.get(gamesUrl, gamesList => callback(gamesList))
  }

}
