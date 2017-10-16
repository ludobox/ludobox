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
  }
}
export default class DropZone extends React.Component {

  onDrop(files) {
    const filesList = [...this.props.files, ...files]
    this.props.handleAddFiles(filesList)
  }

  handleRemoveFile(file) {
    const newFiles = this.props.files
      .filter(f => f.name !== file.name)
    this.props.handleAddFiles(newFiles)
  }

  render() {
    const {files} = this.props;

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
          <div>Try dropping some files here, or click to select files to upload.</div>
        </Dropzone>
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
