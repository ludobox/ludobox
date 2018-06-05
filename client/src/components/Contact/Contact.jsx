import React from 'react'
import SocialMedia from '../SocialMedia/SocialMedia.jsx'

export default class Contact extends React.Component {
  render() {
    
    return (
        <div>
          <img className="full-width-image"
            src="/images/about/ludobox-public-event.jpg"
            alt="Ludobox Public Event"
            />
          <div className="row" style={{paddingTop : '4em'}}>
            <div className="six columns" style={{ textAlign : 'center'}}>
              <h2>Get in touch</h2>
                <h5>
                  <span className="line4">For any questions and inquiries,</span>
                  <br />
                  <span id="contact-text">
                    <a href="mailto:contact@ludobox.net">contact@ludobox.net</a>
                  </span>
                </h5>
            </div>
            <div className="six columns" style={{ textAlign : 'center'}}>
              <h4 className="welcome">
                Find us online
              </h4>
              <SocialMedia showNames={true}/>
            </div>
          </div>
        </div>
    )
  }
}
