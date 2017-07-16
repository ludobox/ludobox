import React from 'react'

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

    if (userProfile.recent_changes)
      userProfile.recent_changes.map( event =>{
        console.log(event)}
        // <li>
        //
        // </li>
      )

    return (
      <div>

        <h5>Welcome to your page</h5>
        <p><b>Email </b>: {userProfile.email}</p>
        <h4>Recent changes</h4>

      </div>
    )
  }
}
