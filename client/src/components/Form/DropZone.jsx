import React from 'react';
import Dropzone from 'react-dropzone';

const style = {
  dropZone : {
    borderWidth: 4,
    borderColor: '#CCC',
    borderStyle: 'dashed',
    borderRadius: 4,
    margin: 30,
    padding: 30,
    width: "80%",
    height: 100,
    transition: 'all 0.5s'
  },
  errors : {
    color : 'red',
    fontSize : '.8em'
  }
}
export default class DropZone extends React.Component {

  constructor(props) {
    super(props)
    this.state = { errors: [] }
  }

  onDrop(files) {

    // check file size
    const maxFileSize =  this.props.maxFileSize* 1000000;// convert to octets

    const errors = []
    files.forEach( f =>
      f.size > maxFileSize ?
        errors.push(`${f.name} is too big and can not be added.`)
        : null
    )
    this.setState({errors})

    let checkedFiles = files.filter(f => f.size < maxFileSize)
    const filesList = [...this.props.files, ...checkedFiles]
    this.props.handleAddFiles(filesList)
  }

  handleRemoveFile(file) {

    this.setState({errors : []})

    const newFiles = this.props.files
      .filter(f => f.name !== file.name)
    this.props.handleAddFiles(newFiles)
  }

  render() {
    const { files, maxFileSize } = this.props;

    const filesItems = files.map( file =>
      <li key={file.name}>
        {file.name}
        <a onClick={() => this.handleRemoveFile(file)}
          style={{cursor : "pointer"}}
          >
          <i className="icono-cross"></i>
        </a>
      </li>
    )



    return (
      <div>
        <Dropzone
          onDrop={this.onDrop.bind(this)}
          style={style.dropZone}
          >
          <div>
            Try dropping some files here, or click to select files to upload.
            <br />
            <br />
            <small>Maximum file size: {maxFileSize} Mo</small>
          </div>
        </Dropzone>
        {
          this.state.errors.length ?
          <ul style={{listStyle:'none'}}>
            {
              this.state.errors.map(err =>(
                <li key={err} style={style.errors}>{err}</li>
              ))
            }
          </ul>
          :
          null
        }
        {
          this.props.files.length ?
          <div>
            <p>Added {this.props.files.length} files.</p>
            <ul>
              {filesItems}
            </ul>
          </div>
          :
            null
        }
      </div>
    )
  }
}
