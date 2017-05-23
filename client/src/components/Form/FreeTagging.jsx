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


export default class FreeTagging extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      items : this.props.items
    }
  }

  handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      let items = [...this.state.items, e.target.value]
      this.setState({ items })
      this.handleChange( items )
      this.refs.newItemInput = ""
    }
  }

  removeItem(item) {
    // remove
    let {items} = this.state
    let i = items.indexOf(item);
    if (i > -1) items.splice(i, 1);

    this.setState({ items })
    this.handleChange(items)
  }

  handleChange(items) {
    this.props.handleChange({ items })
  }

  render() {

    // prevent crashing on null value
    if(!this.props.items) return null

    const lis = this.state.items.map( (item, i) =>
      <li key={i}
        style={styleLi}
        >
        {item}
        { this.props.editing ?
          <a onClick={() => this.removeItem(item)}
            style={{cursor : "pointer"}}
            >
            <i className="icono-cross"></i>
          </a>
          :
          null
        }
      </li>
    )

    return (
      <span>
        <ul style={styleUl}>
          {lis}
        {
          this.props.editing ?
            <li style={
              Object.assign({}, styleLi, {
                padding : "10px 0.5em 0 0.5em"
               })
              }>
              <input
                placeholder="Type sth here..."
                ref="newItemInput"
                onKeyPress={this.handleKeyPress}
              />
            </li>
          :
          null
        }
        </ul>
      </span>
    )

  }
}
