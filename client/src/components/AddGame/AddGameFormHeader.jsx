import React from 'react';
import { Link } from 'react-scroll'


const style = {
  header :  {
    background :"#fff",
    // height: "100px",
    display : "block",
    position: "fixed", /* Set the navbar to fixed position */
    width : "80%",
    top: "6.5rem" /* Position the navbar at the top of the page */
  },
  headerInner : {
    position : "relative",
    paddingTop : "15px"
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
    width : "16%",
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

export default class AddGameFormHeader extends React.Component {

  render () {

    let tabsLi = this.props.tabsItems.map( (d,i)=> (
        <li
          key={d.name}
          style={style.li}
          datatype={d.name}>
          <Link
            activeClass="active"
            className="test1"
            to={d.name}
            smooth={true}
            duration={500}
            style={style.a}
            title={d.name}
            onClick={this.props.handleClickTabMenu.bind(this, d.name)}
            >
            <span
              style={
                d.name === this.props.selectedTab ?
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
          { d.name === this.props.selectedTab ?
            <span style={Object.assign({}, style.caret, { left : (7+i*16)+"%" })}></span>
            :
            null
          }
          </Link>
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
