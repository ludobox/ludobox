import React from 'react';
import schema from '../../../../model/schema.json';
import Form from 'react-jsonschema-form';

import { Events, Element} from 'react-scroll'

import {ToastContainer, ToastMessage} from 'react-toastr';
const ToastMessageFactory = React.createFactory(ToastMessage.animation);

import APIClient from "../../api.js"

import AddGameFormHeader from "./AddGameFormHeader.jsx"
// import TabPanel from "./TabPanel.jsx"
import DropZone from "./DropZone.jsx"

const style = {
  addGameForm : {
    marginTop : "8rem"
  },
  form: {
  }
}

function TabFieldTemplate(props) {
  const {id, classNames, label, help, required, description, errors, children} = props;

  let name = id.split("_").pop('root')
  let isHeader = id.split("_").length === 2;

  let fieldTemplate = isHeader ?
    <Element name={name}>
      {/* <label htmlFor={id}>{label}{required ? "*" : null}</label> */}
      {description}
      {children}
      {errors}
      {help}
    </Element>
    :
    <div className={classNames}>
      {/* <label htmlFor={id}>{label}{required ? "*" : null}</label> */}
      {description}
      {children}
      {errors}
      {help}
    </div>

  return fieldTemplate
}

const uiSchema = {
  "ui:order": [
    'title',
    'description',
    'audience',
    'fabrication',
    'credentials',
    'source',
    'timestamp_add',
    'content_type'
  ],
  "description" : {
    "summary": { "ui:widget": "textarea" },
    // should be default to game for now
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
  "content_type" : { "ui:disabled" : true, "ui:widget": "hidden" },
  "timestamp_add" : { "ui:widget": "hidden" } // added on the server
}

const tabsItems = [
  {
    name : "files",
    icon : "icono-folder"
  },
  {
    name : "description",
    icon : "icono-document"
  },
  {
    name : "audience",
    icon : "icono-user"
  },
  {
    name : "credentials",
    icon : "icono-tag"
  },
  {
    name : "source",
    icon : "icono-asterisk"
  },
  {
    name : "fabrication",
    icon : "icono-market"
  }
]


export default class AddGame extends React.Component {

  constructor(props) {
    super(props)
    this.api = new APIClient()
    this.state = {
      selectedTab : "files", // default to files
      files : [],
      info : {}
    };
  }

  handleClickTabMenu(name) {
    this.setState({selectedTab : name });
  }

  handleAddFiles(files) {
    this.setState({files : files });
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
      <div>
        <ToastContainer ref="container"
            toastMessageFactory={ToastMessageFactory}
            className="toast-top-right" />
        <h3>Add a new game !</h3>


        <AddGameFormHeader
          handleClickTabMenu={this.handleClickTabMenu.bind(this)}
          selectedTab={this.state.selectedTab}
          tabsItems={tabsItems}
          />
        <div
          className="addGameForm"
          style={style.addGameForm}
          >
          <h4>Add a new game</h4>
          <Element id="files">
            <DropZone
              handleAddFiles={this.handleAddFiles.bind(this)}
            />
          </Element>
          <Form
            schema={schema}
            uiSchema={uiSchema}
            formData={this.state.info}
            // onChange={this.success.bind(this)}
            FieldTemplate={TabFieldTemplate}
            onSubmit={ this.onSubmit.bind(this)}
            onError={ ({errors}) => this.errors.bind(this, errors)}
            />
        </div>
      </div>
    )
  }
}
