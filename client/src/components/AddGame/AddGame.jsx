import React from 'react';
import schema from '../../../../ludobox/model/schema.json';
import Form from 'react-jsonschema-form';
import Dropzone from 'react-dropzone';

import {ToastContainer, ToastMessage} from 'react-toastr';
console.log(schema);
const ToastMessageFactory = React.createFactory(ToastMessage.animation);

const uiSchema = {
  "ui:order": [
    'title',
    'description',
    'audience',
    'fabrication',
    'credentials',
    'source',
    'timestamp_add'
  ],
  "description" : {
    "summary": { "ui:widget": "textarea" },
    // should be default to game for now
    "content_type" : { "ui:disabled" : true, "ui:widget": "hidden" }
  },
  "audience" : {
    "age": { "ui:widget": "checkboxes", "ui:options": { inline: true }},
    "number_of_players": {
      "players_min": { "ui:widget": "range" },
      "players_max": { "ui:widget": "range" },
    },
    "duration": { "ui:widget": "updown" },
  },
  "credentials" : {
    "publication_year": { "ui:widget": "updown" }
  },
  "fabrication" : {
    "fab_time": { "ui:widget": "updown" }
  },
  "source"  : {
    "url": { "ui:widget": "uri" }
  },
  "timestamp_add" : { "ui:widget": "hidden" } // added on the server
}

export default class AddGame extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      files : [],
      info : {}
    };
  }

  onDrop(files) {
    console.log(files);
    this.setState({
      files: [...this.state.files, ...files]
    });
  }

  success() {
    console.log(this);
    this.refs.container.success(
      "You have successfully added a new game.",
      "Congrats !",
      {
      closeButton:true,
      timeOut: 5000

    });
  }

  errors(errors) {
    console.log("errors");
    this.refs.container.error(
        errors.toString(),
        "There is errors...",
      {
        closeButton:true
      });
  }

  render() {

    return (
      <span>
        <h3>Add a new game !</h3>
        <Dropzone onDrop={this.onDrop.bind(this)}>
          <div>Try dropping some files here, or click to select files to upload.</div>
        </Dropzone>
        {
          this.state.files ?
          <div>
            <p>Uploading {this.state.files.length} files...</p>
            <ul>
              {this.state.files.map( file =>  <li>{file.name}</li> )}
            </ul>
          </div>
          :
            null
        }
        {/* <ToastContainer ref="container"
            toastMessageFactory={ToastMessageFactory}
            className="toast-top-right" /> */}

        <Form
          schema={schema}
          uiSchema={uiSchema}
          // onChange={this.success.bind(this)}
          onSubmit={this.success.bind(this)}
          onError={this.errors.bind(this)} />

      </span>
    )
  }
}
