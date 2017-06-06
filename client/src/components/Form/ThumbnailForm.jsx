import React, {Component} from 'react';
import Cropper from 'react-cropper';

const src = '/images/ludobox-logo-color2.png';

export default class ThumbnailForm extends Component {

  constructor(props) {
    super(props);
    this.state = {
      src,
      cropResult: null,
    };
  }

  preview(e) {
    e.preventDefault();
    if (typeof this.cropper.getCroppedCanvas() === 'undefined') {
      return;
    }

    this.setState({
      cropResult: this.cropper.getCroppedCanvas().toDataURL(),
    });
  }

  saveImage(e) {
    e.preventDefault();
    // convert URI to File using Blob
    let blob = dataURItoBlob(this.state.cropResult)
    let f = new File([blob], "thumbnail.png");

    // send files to server
    this.props.handleAddFiles([f])
  }

  onChange(e) {
    e.preventDefault();
    let files;
    if (e.dataTransfer) {
      files = e.dataTransfer.files;
    } else if (e.target) {
      files = e.target.files;
    }
    const reader = new FileReader();
    reader.onload = () => {
      this.setState({ src: reader.result });
    };
    reader.readAsDataURL(files[0]);
  }

  render() {
    return (
      <div>
        <label>Select an image
          <input type="file" onChange={e => this.onChange(e)} />
        </label>
        <Cropper
          style={{ height: 400, width: '100%' }}
          aspectRatio={16 / 9}
          preview=".img-preview"
          guides={false}
          src={this.state.src}
          ref={cropper => { this.cropper = cropper; }}
          />
        <a className="button"
          onClick={ e =>this.preview(e)}
          >
          Preview
        </a>
        <img style={{ width: '100%' }}
          src={this.state.cropResult}
          alt="cropped image"
          />
        <a className="button"
          onClick={ e => this.saveImage(e)}
          >
          Save Thumbnail
        </a>
      </div>
    );
  }
}

function dataURItoBlob(dataURI) {
    // convert base64/URLEncoded data component to raw binary data held in a string
    var byteString;
    if (dataURI.split(',')[0].indexOf('base64') >= 0)
        byteString = atob(dataURI.split(',')[1]);
    else
        byteString = unescape(dataURI.split(',')[1]);

    // separate out the mime component
    var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];

    // write the bytes of the string to a typed array
    var ia = new Uint8Array(byteString.length);
    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }

    return new Blob([ia], {type:mimeString});
}
