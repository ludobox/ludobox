import React from 'react'
import moment from 'moment'

export default class History extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      showDetails : false
    }

  }

  showDetails() {
    this.setState({showDetails : !this.state.showDetails})
  }
  render() {
    const history = this.props.history ? this.props.history : []

    const events = history.map( event => {
      // parse date
      let d = moment
        .utc(event.ts*1000)
        .local()
        .format('MMMM Do YYYY, h:mm:ss a');
      return (
        <li key={event.id}>
          <a href={`#${event.id}`}>
            {event.type}d
          </a> by {event.user} on {d}
        </li>
      )
    })
    const { showDetails } = this.state

    return (
      <span>
        <p>{this.props.history.length} modifications
          <a onClick={() => this.showDetails()}>
            {
              showDetails ?
              "(Hide details)"
              :
              "(Show details)"
            }
          </a>
        </p>

        {
          showDetails ?
          <ul>
            {events}
          </ul>
          :
          null
        }
      </span>
    )
  }
}
