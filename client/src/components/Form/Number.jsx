import React from 'react'

export default class Number extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      text : null,
      editing : false,
      value : this.props.defaultValue
    }
  }

  handleChange(e) {
    this.setState({ value : e.target.value });
    this.props.handleChange({value : e.target.value})
  }

  render() {

    return (
      this.props.editing ?
        <input
          onChange={ e => this.handleChange(e)}
          value={this.state.value}
          type="number"
        />
      :
      <span>
        {this.state.value}
      </span>
    )
  }
}
