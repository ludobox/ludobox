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

  render() {
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
              {this.props.files.map( file =>  <li key={file.name}>{file.name}</li> )}
            </ul>
          </div>
          :
            null
        }
      </div>
    )
  }
}
