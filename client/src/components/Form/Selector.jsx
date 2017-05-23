import React from 'react'

export default class Selector extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      text : null,
      editing : false,
      optionsState : this.props.defaultValue
    }
  }

  handleChange(e) {
    this.setState({ optionsState : e.target.value });
    this.props.handleChange({value : e.target.value})
  }

  render() {

    let {editing} = this.props
    let {optionsState} = this.state

    let options = this.props.options.map( (o,i) =>
      <option key={i} value={o}>{o}</option>
    )
    return (
      editing ?
        <select
          value={this.state.optionsState}
          onChange={ e => this.handleChange(e)}
          >
          {options}
        </select>
      :
      <span>
        {optionsState}
      </span>
    )
  }
}
