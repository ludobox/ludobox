import React from 'react';
import schema from '../../../../ludobox/model/schema.json';
import Form from 'react-jsonschema-form';

import {ToastContainer, ToastMessage} from 'react-toastr';
console.log(schema);
const ToastMessageFactory = React.createFactory(ToastMessage.animation);

export default class AddGame extends React.Component {

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
        <ToastContainer ref="container"
            toastMessageFactory={ToastMessageFactory}
            className="toast-top-right" />
        <p>Add a new game !</p>
        <Form schema={schema}
          // onChange={this.success.bind(this)}
          onSubmit={this.success.bind(this)}
          onError={this.errors.bind(this)} />

      </span>
    )
  }
}
