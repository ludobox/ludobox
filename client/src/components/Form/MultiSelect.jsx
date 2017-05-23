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

  handleChange(e) {
     const items = [...e.target.options]
      .filter(o => o.selected)
      .map(o => o.value)

      this.props.handleChange( items )
  }

  render() {

    // prevent crashing on null value
    if(!this.props.value) return null

    const lis = this.props.value.map( (item, i) =>
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
              value={this.props.selected}
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
