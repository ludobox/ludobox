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
    console.log(userProfile)

    let history = []
    if (userProfile.recent_changes)
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

    return (
      <div>

        <h5>Welcome to your page</h5>
        <p><b>Email </b>: {userProfile.email}</p>
        <h4>Recent changes</h4>
        {
          history.length ?
            history
          :
            "No history to show."
        }

      </div>
    )
  }
}
