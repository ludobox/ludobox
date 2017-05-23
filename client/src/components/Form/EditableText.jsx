import React from 'react'
import Markdown from 'react-remarkable'

const styles = {
  helpBlock : {
    color : "#CCC",
    fontSize: '.8em'
  }
}

export default class EditableText extends React.Component {

  handleChange(e) {
    // pass back changes to parent Component
    this.props.handleChange(e.target.value)
  }

  componentDidMount() {
    document.addEventListener('keydown', this.handleKeyPress);
  }

  render() {
    if ( this.props.editing ) {
      return (
        <span>
          {this.props.type === 'input' ?
            <input
              type={this.props.fieldType ? this.props.fieldType : "text"}
              value={this.props.text || ""}
              onChange={(e) => this.handleChange(e)}
              name={this.props.fieldId}
              placeholder={this.props.placeholder}
              ref="textField"
              style={this.props.error ? {borderColor: 'red'} : null}
            />
          : null}
          {this.props.type === 'textarea' ?
            <span style={this.props.style}>
              <span style={styles.helpBlock}>
                Format with <a href="http://www.markdowntutorial.com/" target="_blank">Markdown</a>.
              </span>
              <textarea
                rows={15}
                style={this.props.error ?
                  {height : '30%', borderColor: 'red'}
                  :
                  {height : '30%'}
                }
                value={this.props.text}
                placeholder={this.props.placeholder}
                onChange={(e) => this.handleChange(e)}
                name={this.props.fieldId}
                ref="textField"
              />
            </span>
          :
          null}
          {
            this.props.error ?
            <span style={{fontSize:'10pt', color : 'red'}}>
              { this.props.error }
            </span>
            :
            null
          }

        </span>
      )
    }
    else {
      let text = (this.props.text == '') ? this.props.placeholder : this.props.text
      let className = 'editable'
      if (this.props.type === 'textarea') {
        text =  <Markdown>{this.props.text}</Markdown>
        className += ' markdown-body'
      }
      if (this.props.text == '') className +=' emptyfield'
      return (
        <span
          className={className}
        >
          {text}
        </span>
      )
    }
  }
}
