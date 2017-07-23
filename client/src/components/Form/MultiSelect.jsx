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
    // parse display name
    this.opts =  {}
    this.props.options.map( d => this.opts[d.value] = d.name )
  }

  handleChange(e) {
     const items = [...e.target.options]
      .filter(o => o.selected)
      .map(o => o.value)

      this.props.handleChange( items )
  }

  render() {

    const error = this.props.error ?
      <span style={{fontSize:'10pt', color : 'red'}}>
        { this.props.error }
      </span>
      :
      null

    const lis = this.props.value ?
      this.props.value.map( (item, i) =>
        <li key={i}
          style={styleLi}
          >
          {this.opts[item]}
        </li>
      )
      :
      null

    const options = this.props.options.map( (item,i) =>
      <option key={i} value={item.value}>{item.name}</option>
    )

    let style= { height: '20%'};

    return (
      <span>
        {
          this.props.editing ?
            <select
              multiple
              size={8}
              style={
                this.props.error ?
                Object.assign(style, {borderColor: 'red'})
                :
                style
              }
              onChange={ (e) => this.handleChange(e)}
              value={this.props.value}
              >
              {options}
            </select>
          :
            <ul style={styleUl}>
              {lis}
            </ul>
        }
        { this.props.error ? error : null}
      </span>
    )

  }
}
