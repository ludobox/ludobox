import React from 'react'

import DropZone from './DropZone.jsx'

export default class FilesList extends React.Component {

  removeFile(file) {
    let confirmFileDeletion = confirm("Are you sure you want to delete this file?");
    if (confirmFileDeletion === true) {
      this.props.handleDeleteFile(file.filename)
    }
  }

  render() {

    const {
      handleFileUpload,
      editing
    } = this.props

    let uploader = handleFileUpload ?
      <a className="button"
        onClick={files => handleFileUpload(files)}
        >Upload Files
      </a>
      :
      null

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

        { editing ?
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

    const newFiles = this.props.newFiles || []

    return (
      <span>
        <ul>
          {files}
        </ul>
        {this.props.editing ?
          <span>
            <DropZone
              files={newFiles} // pass new files to be added
              handleAddFiles={files => this.props.handleAddFiles(files)}
            />
            {uploader}
          </span>
          :
          null
        }
      </span>
    )
  }
}
