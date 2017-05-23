import React from 'react'

import DropZone from './DropZone.jsx'

export default class FilesList extends React.Component {

  removeFile() {
    let confirmFileDeletion = confirm("Are you sure you want to delete this file?");
    if (confirmFileDeletion === true) {
      // TODO : add a file
      console.log("File is going to be deleted from the server.")
    }
  }

  render() {
    let files = this.props.files.map( file =>
      <li key={file.filename}>
        <a
          href={file.url}
          title={file.filename}
          >
          {
            `${file.filename.substring(0, 8)}... (${file.filename.split('.').pop().toUpperCase()})`
          }
        </a>

        { this.props.editing ?
          <a onClick={() => this.removeFile(file)}
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
        <ul>
          {files}
        </ul>
        {this.props.editing ?
          <DropZone />
          :
          null
        }
      </span>
    )
  }
}
