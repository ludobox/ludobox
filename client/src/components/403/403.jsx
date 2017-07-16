import React from 'react'

export default class Page403 extends React.Component {
  render() {
    return (
      <div>
        <h1>Ludobox</h1>
        <p>Sorry, you need to be logged in to do this.</p>

        <p>
          <a href="/login">Login</a> or <a href="/register">Register</a>
        </p>
      </div>
    )
  }
}
