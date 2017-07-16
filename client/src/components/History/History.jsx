import React from 'react'

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

    const lis = history.map( event =>
      <li key={event.ts}>{event.ts}</li>
    )
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
            {lis}
          </ul>
          :
          null
        }
      </span>
    )
  }
}
