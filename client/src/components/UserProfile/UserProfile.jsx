import React from 'react'

import moment from 'moment'

import APIClient from "../../api.js"

export default class UserProfile extends React.Component {

  constructor(props) {
    super(props)
    this.api = new APIClient()
    this.state = {
      userProfile: {}
    };
  }

  fetchUserProfile() {
    let userId = this.props.userId;
    this.api.getUserProfile(
      userId,
      userProfile => this.setState({ userProfile })
    );
  }

  componentDidMount() {
    this.fetchUserProfile()
  }

  render() {
    let { userProfile } = this.state

    let roles, history;

    let profileReady = Object.keys(userProfile).length;

    if (profileReady) {
      console.log(userProfile)
      roles = userProfile.roles.join(", ")
      history = userProfile.recent_changes.map( event =>{
        // parse date
        let d = moment
          .utc(1234567890000)
          .local()
          .format('MMMM Do YYYY, h:mm:ss a');

        return (
          <li key={event.event.id}>
            <b>{event.event.type}</b> : <a href={`/games/${event.slug}`}>{event.title}</a> : {d}
          </li>
        )
      }
      )
    }

    return (
      <div>

        <h3>Welcome to your page</h3>
        {
          profileReady ?
          <p>
            <b>Email </b>: {userProfile.email}
            <br />
            <b>Roles </b>: {roles}
          </p>
          :
          null
        }
        <h5>Recent changes</h5>
        {
          history ?
            history
          :
            "No history to show."
        }

      </div>
    )
  }
}
