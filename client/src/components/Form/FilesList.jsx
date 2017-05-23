import React from 'react'

export default class FilesList extends React.Component {

  render() {
    console.log();
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
      </li>
    )

    return (
      <span>
        <ul>
          {files}
        </ul>
      </span>
    )
  }
}
