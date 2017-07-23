import React from 'react'


const states = {
  "needs_review" : {
    text : "Needs Review",
    color : "orange"
  },
  "validated" : {
    text : "Validated",
    color : "green"
  },
  "rejected" : {
    text : "Rejected",
    color : "red"
  }
}

const style = {
  border : "1px solid #ccc",
  borderRadius : "5px",
  fontSize : ".7em",
  padding : ".5em 1em"
}

export default class ContentState extends React.Component {
  render() {

    let {state, errors} = this.props;

    if (!errors) errors = []

    let text = errors.length ?
      `${errors.length} errors `
      :
      states[state].text

    let color = errors.length ?
      "red"
      :
      states[state].color


    return (
      <span style={Object.assign(style, {color, borderColor : color})}>
        {text}
      </span>
    )
  }
}
