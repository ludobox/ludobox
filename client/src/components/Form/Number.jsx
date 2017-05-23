import React from 'react'

export default class Number extends React.Component {

  handleChange(e) {
    this.props.handleChange(parseInt(e.target.value))
  }

  render() {

    const error = this.props.error ?
      <span style={{fontSize:'10pt', color : 'red'}}>
        { this.props.error }
      </span>
      :
      null

    return (
      this.props.editing ?
      <span>
        <input
          style={this.props.error ? {borderColor: 'red'} : null}
          onChange={ e => this.handleChange(e)}
          value={this.props.value}
          type="number"
        />
        {error}
      </span>
      :
      <span>
        {this.props.value}
      </span>
    )
  }
}
