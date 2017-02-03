import React from 'react';

const style = {
  header :  {
    background :"#fff",
    // height: "100px",
    display : "block"
  },
  headerInner : {
    position : "relative"
  },
  connectingLine : {
    position : "absolute",
    height: "2px",
    background: "#e0e0e0",
    top: "40px",
    left: 0,
    right: 0,
    margin: "0 auto",
    zIndex: 1,
    width: "80%"
  },
  ul : {
    listStyle  : "none",
    position : "relative",
    paddingBottom: "20px",
    borderBottom: "1px solid #ccc"
  },
  li : {
    display: "inline-block",
    listStyleType: "none",
    width : "20%",
    margin: 0,
    textAlign: "center"
  },
  a : {
    padding : 0,
    left: 0,
    borderRadius: "70px",
    width: "70px",
    height: "70px",
  },
  round : {
    zIndex: 2,
    position : "relative",
    display: "block",
    borderRadius: "70px",
    width: "70px",
    height: "70px",
    lineHeight: "70px",
    display: "inline-block",
    background: "#fff",
    textAlign: "center"
  },
  icon: {
    color: "#333",
    top : "15px"
  },
  caret : {
    position: "absolute",
    opacity: 1,
    margin: "0 auto",
    bottom: "0px",
    border: "10px solid transparent",
    borderBottomColor: "#5bc0de",
  }
}

const types = [
  {
    name : "files",
    icon : "icono-folder"
  },
  {
    name : "description",
    icon : "icono-document"
  },
  {
    name : "audience",
    icon : "icono-user"
  },
  {
    name : "credentials source",
    icon : "icono-asterisk"
  },
  {
    name : "fabrication",
    icon : "icono-market"
  }
]

export default class AddGameFormHeader extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      selected : "files" // default to files
    }
  }

  handleClick(name) {
    console.log(name);
    this.setState({selected : name });
  }

  render () {

    let tabsLi = types.map( (d,i)=> (
      <li
        key={d.name}
        style={style.li}
        datatype={d.name}>
        <a
          style={style.a}
          title={d.name}
          onClick={this.handleClick.bind(this, d.name)}
          >
          <span
            style={
              d.name === this.state.selected ?
                Object.assign({}, style.round, { borderColor : "#5bc0de"})
              :
              style.round
            }
            className="form-menu-item"
            >
            <i
              className={d.icon }
              style={style.icon}
              >
            </i>
          </span>
        </a>
        { d.name === this.state.selected ?
          <span style={Object.assign({}, style.caret, { left : (8+i*20)+"%" })}></span>
          :
          null
        }
      </li>
    ))

    return (
      <header className="form-header" style={style.header}>
        <div style={style.headerInner}>
        <div className="horizontal-line" style={style.connectingLine}></div>
          <ul style={style.ul}>
            {tabsLi}
          </ul>
        </div>
      </header>
    )

  }
}
