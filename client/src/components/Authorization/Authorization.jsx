import React from 'react'
import {browserHistory} from 'react-router'
import Page403 from '../403/403.jsx'

// Authorization HOC
export const Authorization = (allowedRoles) =>
  (WrappedComponent) =>
    class extends React.Component {

      constructor(props) {
        super(props)
        this.state = {
          user: { }
        }
      }

      componentDidMount() {
        let { user } = window.initialData
        this.setState({ user })
        console.log(user);
      }

      render() {
        const { roles } = this.state.user
        let isAuthorized = false;

        if(roles)
          isAuthorized = allowedRoles.filter(function(n) {
              return roles.indexOf(n) !== -1;
          }).length != 0

        if (isAuthorized) {
         return <WrappedComponent {...this.props} />
        }
        else {
          return <Page403 />
        }
      }
    }
