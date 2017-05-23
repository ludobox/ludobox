import React from 'react'

const styleLi = {
  // display : "inline",
  padding : "0 .5em",
  margin : ".5em ",
  width: "auto",
  lineHeight: "2.5em",
  display: "inline-block",
  border : "1px solid #ccc"
},
styleUl = { listStyle : "none"}


export default class MultiSelect extends React.Component {

  constructor(props) {
    super(props)
    console.log(this.props.defaultValue);
    this.state = {
      selected : this.props.defaultValue
    }
  }

  handleChange(e) {
    console.log(e.target.value);

     const items = [...e.target.options]
      .filter(o => o.selected)
      .map(o => o.value)

      this.setState({ selected : items })
      this.props.handleChange({ items })
  }

  render() {

    // prevent crashing on null value
    if(!this.state.selected) return null

    const lis = this.state.selected.map( (item, i) =>
      <li key={i}
        style={styleLi}
        >
        {item}
      </li>
    )

    const options = this.props.options.map( (item,i) =>
      <option key={i} value={item}>{item}</option>
    )

    return (
      <span>
        {
          this.props.editing ?
            <select
              multiple
              size={8}
              style={{ height: '20%'}}
              onChange={ (e) => this.handleChange(e)}
              value={this.state.selected}
              >
              {options}
            </select>
          :
            <ul style={styleUl}>
              {lis}
            </ul>
        }
      </span>
    )

  }
}
