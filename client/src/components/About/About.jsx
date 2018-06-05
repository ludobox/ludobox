import React from 'react'
import './about.scss'
import PageTitle from '../PageTitle/PageTitle.jsx'

export default class AboutPage extends React.Component {

  render() {

    const { version } = this.props.config

    return (
      <main id="about">
        <section id="intro" className="row">
          <header className="six columns">
            <h1 className="ludobox-logo logo" >
              Ludobox
            </h1>
          </header>
          <div id="description" className="six columns">
            <div className="container">
              <h5>
                The <b>Ludobox</b> is an electronic device that distributes printable games into the public space.
                <br />
                <br />
                <small>
                  Each box contains dozens of digital files and instructions to make your own games and turns any place into a game library.
                </small>
              </h5>
            </div>
          </div>
        </section>
        <img className="full-width-image"
          src="/images/about/ludobox-box-web.jpg"
          alt="Ludobox Box Image"
          />
        <section id="make">
          <img className="punchline"
            src="/images/ludobox-punchline1.png"
            alt="Punchline"
            />
          <h5>
            <span className="main">Print'n play are games that you can make by yourself.</span>
            <br />
            <small>
              <span className="line1">From a card game in PDF using a printer and scissors</span>
              <br />
              <span className="line2">to a board game accessing a 3D printer to reproduce tokens,</span>
              <br />
              <span className="line3">Ludobox invites to materialize & craft digital files.</span>
            </small>
          </h5>
          <img className="fab"
            src="/images/about/fablab_machinescfao2.png"
            alt=""
            />
        </section>
        <img className="full-width-image"
          src="/images/about/ludobox-event-play-web.jpg"
          alt="Ludobox Box Image"
          />
        <section id="download">
          <h3 className="title">Make your own Box</h3>
          <div className="container">
            <h5>
              <span className='line1'>
                You can build your own box from scratch
              </span>
              <br />
              <span className="line2">
                and directly download games from our online collection.
              </span>
            </h5>
          </div>
          <p className="doclink">
            <a href="https://hackmd.io/s/Skje3bygW" className="button" target="_blank">Create your own Box</a>
            <br />
          </p>
          <p className="links">
            Check <a href="https://github.com/ludobox/ludobox">the code</a> or read <a href="https://wiki.ludobox.net">the docs</a>
          </p>
        </section>
        <img className="full-width-image"
          src="/images/about/ludobox-workshop-kids.jpg"
          alt="Ludobox Kids Workshop"
          />
        <section id="contact" className="container" >
          <h3>Get in Touch</h3>
          <h5>
            <span className="line1">Interested in installing a Ludobox ?</span>
            <br />
            <span className="line2">Organizing a game festival ?</span>
            <br />
            <span className="line3">Experimenting with collaboration and games?</span>
            <br />
            <span className="line4">Inventing or publishing open-source games?</span>
            <br />
            <br />
            <span id="contact-text">Contact us at :</span> <a href="mailto:contact@ludobox.net">contact@ludobox.net</a>
          </h5>
        </section>
        <hr />
        <footer className="site-footer">
          <p className="support">
            This project is powered by <a className="no-external" href="http://dcalk.org" target="_blank"><b>DCALK</b>.</a>
            <br />
            <small>It was made possible with the support of</small>
          </p>
          <ul id="logos">
            <li>
              <a className="no-external" href="http://www.institutfrancais.com">
                <img src="/images/logos/250px-Institut-francais.png" />
              </a>
            </li>
            <li>
              <a className="no-external" href="http://www.culturalfoundation.eu">
                <img src="/images/logos/European-Culture-Fondation-@-Laculture.info_.png" />
              </a>
            </li>
            <li>
              <a className="no-external" href="http://www.culturecommunication.gouv.fr">
                <img src="/images/logos/logo mcc.jpg" />
              </a>
            </li>
            <li>
              <a className="no-external" href="https://funlab.fr">
                <img src="/images/logos/la-fabrique-d-usages-numeriques.png" />
              </a>
            </li>
            <li>
              <a className="no-external" href="http://www.museecarteajouer.com/">
                <img src="/images/logos/logo-musée-Issy.png" />
              </a>
            </li>
            <li>
              <a className="no-external" href="http://www.makery.info">
                <img src="/images/logos/makery_logo_white.png" />
              </a>
            </li>
          </ul>

          <div className="container">
            <p>
              <br />
              <br />
              <a className="no-external" id="license" target="_blank" rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
                <img alt="Licence Creative Commons"
                  style={{borderWidth:0}} src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png"
                  />
              </a>
            </p>
          </div>
        </footer>

        <p style={{textAlign:"right"}}>
          v{version}
        </p>
      </main>
    )
  }
}
