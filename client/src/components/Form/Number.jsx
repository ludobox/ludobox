import React from 'react'

export default class Number extends React.Component {

  handleChange(e) {
    this.props.handleChange(e.target.value)
  }

  render() {

    return (
      this.props.editing ?
        <input
          onChange={ e => this.handleChange(e)}
          value={this.props.value}
          type="number"
        />
      :
      <span>
        {this.props.value}
      </span>
    )
  }
}
