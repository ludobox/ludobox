import React from 'react'

import APIClient from "../../api.js"
import History from "../History/History.jsx"
import moment from 'moment'

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
      history = userProfile.recent_changes.map( event => {

        // parse date
        let d = moment
          .utc(event.event.ts*1000)
          .local()
          .format('MMMM Do YYYY, h:mm:ss a');
        return (
          <li key={event.event.id}>
            <b>{event.event.type}</b> : <a href={`/games/${event.slug}`}>{event.title}</a> : {d}
          </li>
        )
      })
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
        <h5>Recent Actions</h5>
        {
          history ?
            <ul>
              {history}
            </ul>
          :
            "No history to show."
        }

      </div>
    )
  }
}
