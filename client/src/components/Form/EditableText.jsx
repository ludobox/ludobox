import React from 'react'
import Markdown from 'react-remarkable'

const styles = {
  helpBlock : {
    color : "#CCC",
    fontSize: '.8em'
  }
}

class EditableText extends React.Component {

  constructor(props) {
    super(props)

    this.state = {
      editing: false,
      originalText: this.props.defaultValue, // store initial text
      text : this.props.defaultValue
    }
    this.handleEditToggle = this.handleEditToggle.bind(this)
    this.handleChange = this.handleChange.bind(this)
    this.handleKeyPress = this.handleKeyPress.bind(this)
  }

  handleEditToggle() {
    if (!this.props.allowEmpty && this.state.text == '') {
      console.log( 'This field should not be empty' )
    }
    else this.setState({ editing: !this.state.editing })
  }

  handleChange(e) {
    this.setState({ text: e.target.value })
  }

  componentDidMount() {
    document.addEventListener('keydown', this.handleKeyPress);
  }

  // handle esc
  handleKeyPress(e) {
    const type = this.props.type || 'input'

    if(e.keyCode === 27) this.setState({ editing : false })

    if (
      type === 'input' && e.key === 'Enter'
      ||
      type === 'textarea' && e.key === 'Enter' && e.ctrlKey == true
    ) {
      if (!this.props.allowEmpty && this.state.text == '') {
        console.log('This field should not be empty !')
      }
      else {
        console.log("Save the content.")
        this.props.saveChanges({
          id : this.props.fieldId,
          text : this.state.text
        })
        this.setState({editing : false})
      }
    }

  }

  render() {


    const isModified = this.state.originalText !== this.state.text

    if ( this.state.editing ) {
      return (
        <span>
          {this.props.type === 'input' ?
            <input
              value={this.state.text}
              onChange={this.handleChange}
              onKeyPress={this.handleKeyPress}
              onBlur={this.handleEditToggle}
              name={this.props.fieldId}
              ref="textField"
              style={this.props.style}
            />
          : null}
          {this.props.type === 'textarea' ?
            <span style={this.props.style}>
              <textarea
                rows={15}
                value={this.state.text}
                onChange={this.handleChange}
                onKeyPress={this.handleKeyPress}
                onBlur={this.handleEditToggle}
                name={this.props.fieldId}
                ref="textField"
              />
              <span style={styles.helpBlock}>
                Format with Markdown. Ctrl + enter to validate.
              </span>
            </span>
          : null}
        </span>
      )
    }
    else {
      let text = (this.state.text == '') ? this.props.placeholder : this.state.text
      let className = 'editable'
      if (this.props.type === 'textarea') {
        text =  <Markdown>{this.state.text}</Markdown>
        className += ' markdown-body'
      }
      if (this.state.text == '') className +=' emptyfield'
      return (
        <span
          className={className}
          style={ isModified ? {background : "rgba(30,100,10,.2)"} : null}
        >
          {text}
          <small style={{fontSize:"10pt", cursor : "pointer"}}>
            <a onClick={this.handleEditToggle}>(EDIT)</a>
          </small>
        </span>
      )
    }
  }
}

EditableText.propTypes = {
  /**
  * Select if you want a simple input/text or a multiline markdown/textara field
  */
  type: React.PropTypes.oneOf(['input', 'textarea']),
  /**
  * Default text to be passed at initialization
  */
  defaultValue : React.PropTypes.string,
  /**
  * What is displayed when the text box is empty
  */
  placeholder: React.PropTypes.string,
  allowEmpty: React.PropTypes.bool,
  promptSnackbar: React.PropTypes.func
}


EditableText.defaultProps = {
  allowEmpty: false,
  placeholder : 'Click to edit',
  type : 'input'
}


export default EditableText
