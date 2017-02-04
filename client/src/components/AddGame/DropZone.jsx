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
    height: 300,
    transition: 'all 0.5s'
  }
}
export default class DropZone extends React.Component {

  constructor(props) {
    super(props)
    this.state = { files : [] }
  }

  onDrop(files) {
    console.log(files);
    this.setState({
      files: [...this.state.files, ...files]
    });
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
          this.state.files ?
          <div>
            <p>Uploading {this.state.files.length} files...</p>
            <ul>
              {this.state.files.map( file =>  <li key={file.name}>{file.name}</li> )}
            </ul>
          </div>
          :
            null
        }
      </div>
    )
  }
}
