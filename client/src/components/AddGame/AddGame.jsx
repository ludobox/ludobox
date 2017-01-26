import React from 'react';
import schema from '../../../../ludobox/model/schema.json';
import Form from 'react-jsonschema-form';
import Dropzone from 'react-dropzone';

import {ToastContainer, ToastMessage} from 'react-toastr';
const ToastMessageFactory = React.createFactory(ToastMessage.animation);

import CustomFieldTemplate from './FieldTemplate.jsx';

import APIClient from "../../api.js"

const style = {
  form: {
    columnCount: 3
  },
  dropZone : {
    borderWidth: 4,
    borderColor: '#CCC',
    borderStyle: 'dashed',
    borderRadius: 4,
    margin: 30,
    padding: 30,
    width: 500,
    height: 300,
    transition: 'all 0.5s'
  }
}

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
    this.api = new APIClient()
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

  onSubmit(resp){
    console.log("yay I'm valid!")
    this.setState({ info : resp.formData })
    if( ! this.state.files.length)
      this.refs.container.error(
          "Please add a file...",
          "No files attached",
        {
          closeButton:true,
          handleOnClick: function() { console.log("click") }
        }
      )
    else {
      // POST
      console.log(`ok, let's post that info with ${this.state.files.length} files !`)

      this.api.postGame(resp.formData, this.state.files, (resp) =>
        console.log(resp)
      )
    }

  }

  errors(errors) {
    console.log("errors");

    // this.refs.container.error(
    //     errors.toString(),
    //     "There is errors...",
    //   {
    //     closeButton:true
    //   });
  }

  render() {

    return (
      <span>
        <h3>Add a new game !</h3>
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
        <ToastContainer ref="container"
            toastMessageFactory={ToastMessageFactory}
            className="toast-top-right" />

        <Form
          schema={schema}
          uiSchema={uiSchema}
          formData={this.state.info}
          // onChange={this.success.bind(this)}
          // FieldTemplate={CustomFieldTemplate}
          onSubmit={ this.onSubmit.bind(this)}
          onError={ ({errors}) => this.errors.bind(this, errors)}
          />

      </span>
    )
  }
}
