import React from 'react'

import { browserHistory } from 'react-router'
import AlertContainer from 'react-alert'

import { isAuthorized } from '../../roles'
import APIClient from "../../api.js"

const alertOptions = {
  offset: 14,
  position: 'bottom left',
  theme: 'dark',
  time: 5000,
  transition: 'scale'
}

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

  handleClickDelete() {
    let confirmFileDeletion = confirm("Are you sure you want to delete this ?");
    if (confirmFileDeletion === true) {
      this.api.deleteGame(this.props.slug,
        result => {
          browserHistory.push(`/games`)
          this.msg.success("The game has been deleted.")
        },
        error => this.msg.error(error)
      )
    }
  }

  handleClickBackToReview() {
    this.api.backToReviewGame(this.props.slug,
      result => {
        this.props.updateContent()
        this.msg.success("ok : game is back to review !")
      },
      error => this.msg.error(error)
    )
  }

  handleClickValidate() {
    this.api.validateGame(this.props.slug,
      result => {
        this.props.updateContent()
        this.msg.success("bravo : game validated !")
      },
      error => this.msg.error(error)
    )
  }

  handleClickReject() {
    this.api.rejectGame(this.props.slug,
      result => {
        this.props.updateContent()
        this.msg.success("OK : game rejected.")
      },
      error => this.msg.error(error)
    )
  }

  render() {

    let editButton = isAuthorized("edit_game", this.props.user) ?
           <a className="button"
            //  onClick={() => this.handleClickEdit()
             href={`/games/${this.props.slug}/edit`}
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

    let validateButton = isAuthorized("validate_game", this.props.user) && this.props.state !== "validated" ?
            <a className="button"
              style={{color : "green"}}
              onClick={() => this.handleClickValidate()}
              >
              Validate <i className="icono-check"></i>
            </a>
          :
          null

    let rejectButton = isAuthorized("reject_game", this.props.user) && this.props.state !== "rejected"?
            <a className="button"
              style={{color : "red"}}
              onClick={() => this.handleClickReject()}
              >
              Rejects <i className="icono-cross"></i>
            </a>
          :
          null

    let backToReviewButton = isAuthorized("back_to_review_game", this.props.user) && this.props.state !== "needs_review"?
            <a className="button"
              style={{color : "orange"}}
              onClick={() => this.handleClickBackToReview()}
              >
              Back to review
            </a>
          :
          null

    let actionButtons =
      <span className="actions-buttons">
          {editButton}
          {deleteButton}
          <span style={{marginLeft :"2em"}}>
            {backToReviewButton}
            {validateButton}
            {rejectButton}
          </span>
      </span>

    return (
      <div>
      {
        this.props.user.is_auth ?
        actionButtons
        :
        null
      }
      <AlertContainer ref={a => this.msg = a} {...this.alertOptions} />
      </div>
    )
  }
}
