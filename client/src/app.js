import React from 'react'
import { render } from 'react-dom'
import { IndexRedirect, Router, Route, Link, browserHistory } from 'react-router'

// routes
import App from './components/App.jsx'
import Game from './components/Game/Game.jsx'
import GameEdit from './components/GameEdit/GameEdit.jsx'
import Games from './components/Games/Games.jsx'
import AboutPage from './components/About/About.jsx'
import Contact from './components/Contact/Contact.jsx'
import AddGame from './components/AddGame/AddGame.jsx'
import RemoteGames from './components/RemoteGames/RemoteGames.jsx'
import UserProfile from './components/UserProfile/UserProfile.jsx'
import RecentChanges from './components/RecentChanges/RecentChanges.jsx'
import Page404 from './components/404/404.jsx'
import Page403 from './components/403/403.jsx'


// User roles
import {Authorization} from './components/Authorization/Authorization.jsx'

const Contributor = Authorization(['contributor'])
const Editor = Authorization(['contributor','editor', 'superuser'])
const Admin = Authorization(['editor', 'superuser', 'superuser'])

render((
  <Router history={browserHistory}>
    <Route path="/" component={App}>
      <Route path="contact" component={Contact}/>
      <Route path="about" component={AboutPage}/>
      <Route path="create" component={Contributor(AddGame)}/>
      <Route path="download" component={RemoteGames}/>
      <Route path="games" component={Games} />
      <Route path="games/:gameSlug" component={Game}/>
      <Route path="games/:gameSlug/edit" component={Contributor(GameEdit)}/>
      <Route path="recent" component={RecentChanges} />
      <Route path="profile" component={UserProfile} />
      <Route path="unauthorized" component={Page403}/>
      <Route path="*" component={Page404}/>
      <IndexRedirect to="/games" />
    </Route>
  </Router>
), document.getElementById('ludobox'))
