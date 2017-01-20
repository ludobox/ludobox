import React from 'react'
import ReactDOM from 'react-dom'

import App from './components/App.jsx'

const LUDOBOX_REMOTE_ADDRESS = "http://192.168.1.30:8080";

ReactDOM.render(
  <App
    remote_address={LUDOBOX_REMOTE_ADDRESS}
    />,
  document.getElementById('ludobox')
)
