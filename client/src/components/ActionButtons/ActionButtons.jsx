import React from 'react'

import { browserHistory } from 'react-router'

import { isAuthorized } from '../../roles'
import APIClient from "../../api.js"

// edit button
let editButtonStyle = {
  fontSize:"10pt",
  cursor : "pointer"
}

export default class ActionButtons extends React.Component {

  constructor(props) {
    super(props)
    this.api = new APIClient()
  }

  handleClickEdit() {
    browserHistory.push(`/games/${this.props.slug}/edit`)
  }

  handleClickDelete() {
    let confirmFileDeletion = confirm("Are you sure you want to delete this ?");
    if (confirmFileDeletion === true) {
      this.api.deleteGame(this.props.slug,
        result => browserHistory.push(`/games`),
        error => console.log(error)
      )
    }
  }

  render() {

    let editButton = isAuthorized("edit_game", this.props.user) ?
           <a className="button"
             onClick={() => this.handleClickEdit()}
             >
             Edit
           </a>
           :
           null

    let deleteButton = isAuthorized("delete_game", this.props.user) ?

            <a className="button"
              onClick={() => this.handleClickDelete()}
              >
              Delete
            </a>
          :
          null

      let actionButtons =
        <span className="actions-buttons">
            {editButton}
            {deleteButton}
        </span>

    return (
      <div>
      {
        this.props.user.is_auth ?
        actionButtons
        :
        null
      }
    </div>
    )
  }
}
