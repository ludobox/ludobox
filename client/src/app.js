import React from 'react'
import { render } from 'react-dom'
import { IndexRedirect, Router, Route, Link, browserHistory } from 'react-router'

import App from './components/App.jsx'
import Home from './components/Home/Home.jsx'
import Game from './components/Game/Game.jsx'
import Games from './components/Games/Games.jsx'
import AboutPage from './components/About/About.jsx'
import AddGame from './components/AddGame/AddGame.jsx'
import Page404 from './components/404/404.jsx'

const LUDOBOX_REMOTE_ADDRESS = "http://192.168.1.30:8080";

render((
  <Router history={browserHistory}>
    <Route path="/" component={App} remote_address={LUDOBOX_REMOTE_ADDRESS}>
      <Route path="home" component={Home}/>
      <Route path="about" component={AboutPage}/>
      <Route path="create" component={AddGame}/>
      <Route path="games" component={Games} >
        <Route path="/games/:gameId" component={Game}/>
      </Route>
      <Route path="*" component={Page404}/>
      <IndexRedirect to="/home" />
    </Route>
  </Router>
), document.getElementById('ludobox'))
