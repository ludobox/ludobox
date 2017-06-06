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

  crop(){
    // image in dataUrl
    console.log("cropped")
    // console.log(this.refs.cropper.getCroppedCanvas().toDataURL());
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
    console.log(this.props);
    // this.props.handleFileUpload()
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
