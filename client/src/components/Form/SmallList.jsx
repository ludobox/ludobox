import React from 'react'

export default class SmallList extends React.Component {

  render() {
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

    // prevent crashing on null value
    if(!this.props.items) return null

    const lis = this.props.items.map( (item, i) =>
      <li key={i} style={styleLi}>{item}</li>
    )

    return (
      <ul style={styleUl}>
        {lis}
      </ul>
    )
  }
}
