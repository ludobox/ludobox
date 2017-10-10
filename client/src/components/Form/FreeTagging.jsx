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

  static defaultProps = {
    ...React.Component.defaultProps,
    items: [],
  }

  handleKeyPress = (e) => {
    if (e.key === 'Enter' && e.target.value != '') {
      let items = [...this.props.items, e.target.value]
      this.handleChange( items )
      this.refs.newItemInput.value = ""
    }
  }

  removeItem(item) {
    // remove
    let {items} = this.props
    let i = items.indexOf(item);
    if (i > -1) items.splice(i, 1);

    this.handleChange(items)
  }

  handleChange(items) {
    this.props.handleChange( items )
  }

  render() {

    // prevent crashing on null value
    // if return null

    const lis = (this.props.items) ?
      this.props.items.map( (item, i) =>
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
      :
      null

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
                type="text"
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
