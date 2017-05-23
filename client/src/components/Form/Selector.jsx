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
    const error = this.props.error ?
      <span style={{fontSize:'10pt', color : 'red'}}>
        { this.props.error }
      </span>
      :
      null

    return (
      editing ?
      <span>
        <select
          style={this.props.error ? {borderColor: 'red'} : null}
          value={value}
          onChange={ e => this.handleChange(e)}
          >
          {optionsTags}
        </select>
        {error}
      </span>
      :
      <span>
        {value}
      </span>
    )
  }
}
