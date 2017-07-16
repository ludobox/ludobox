import React from 'react'

import APIClient from "../../api.js"

export default class UserProfile extends React.Component {

  constructor(props) {
    super(props)
    this.api = new APIClient()
    this.state = {
      userProfile: {},
      errors : null
    };
  }

  fetchUserProfile() {
    let userId = this.props.userId;
    this.api.getUserProfile(
      userId,
      userProfile => this.setState({ userProfile }),
      errors => errors ? this.setState({ errors }) : null
    );
  }

  componentDidMount() {
    this.fetchUserProfile()
  }

  render() {
    let { userProfile, errors } = this.state
    // console.log(userProfile, errors)

    return (
      <p>
        Profile
      </p>
    )
  }
}
