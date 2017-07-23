import React from 'react'

export default class Selector extends React.Component {

  constructor(props) {
    super(props)

    // parse display name
    this.opts =  {}
    this.props.options.map( d => this.opts[d.value] = d.name )
  }

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
      <option key={i} value={o.value}>{o.name}</option>
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
          <option value={null}></option>
          {optionsTags}
        </select>
        {error}
      </span>
      :
      <span>
        {this.opts[value]}
      </span>
    )
  }
}
