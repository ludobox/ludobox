import React from 'react'

export default class Selector extends React.Component {

  handleChange(e) {
    this.props.handleChange(e.target.value)
  }

  render() {

    let {
      editing,
      value,
      options
    } = this.props

    let optionsTags = this.props.options.map( (o,i) =>
      <option key={i} value={o}>{o}</option>
    )
    return (
      editing ?
        <select
          value={value}
          onChange={ e => this.handleChange(e)}
          >
          {optionsTags}
        </select>
      :
      <span>
        {value}
      </span>
    )
  }
}
