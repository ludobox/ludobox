import React from 'react'
import './about.scss'
import PageTitle from '../PageTitle/PageTitle.jsx'
import { FormattedMessage, FormattedHTMLMessage, defineMessages } from 'react-intl'

const messages = defineMessages({
    description: {
      id: 'about.description',
      defaultMessage: 'The Ludobox is an electronic device that distributes printable games into the public space.'
    },
    descriptionSmall: {
      id: 'about.description.small',
      defaultMessage: 'Each box contains dozens of digital files and instructions to make your own games and turns any place into a game library.'
    },
    printnplay : {
      main : {
        id : 'about.printnplay.main',
        defaultMessage: "Print'n play are games that you can make by yourself."
      },
      line1: {
        id : 'about.printnplyt.line1',
        defaultMessage: "From a card game in PDF using a printer and scissors"
      },
      line2: {
        id : 'about.printnplay.line2',
        defaultMessage: "to a board game accessing a 3D printer to reproduce tokens,"
      },
      line3: {
        id : 'about.printnplay.line3',
        defaultMessage: "Ludobox invites to materialize & craft digital files."
      }
    },
    make: {
      title : {
        id: 'about.make.title',
        defaultMessage: 'Make your own Box'
      },
      line1: {
        id : 'about.make.line2',
        defaultMessage: "You can build your own box from scratch"
      },
      line2: {
        id : 'about.make.line3',
        defaultMessage: "and directly download games from our online collection."
      },
      button : {
        id : 'about.make.button',
        defaultMessage: "Create your own"
      },
      links : {
        id : 'about.make.links',
        defaultMessage: 'Check <a href="https://github.com/ludobox/ludobox">the code</a> or read <a href="https://wiki.ludobox.net">the docs</a>'
      }
    },
    contact: {
      wiki : {
        id :'about.contact.wiki',
        defaultMessage : 'You’d like to contribute to Ludobox platform ? Visit the <a href="https://wiki.ludobox.net">wiki</a>.'
      }
    },
    footer: {
      credits : {
        id: 'about.footer.credits',
        defaultMessage: 'This project is powered by <a className="no-external" href="http://dcalk.org" target="_blank"><b>DCALK</b>.</a>'
      },
      sponsors : {
        id: 'about.footer.sponsors',
        defaultMessage: 'It was made possible with the support of'
      }
    }
  })

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
                <FormattedMessage {...messages.description} />
                <br />
                <br />
                <small>
                  <FormattedMessage {...messages.descriptionSmall} />
                </small>
              </h5>
            </div>
          </div>
        </section>
        <img className="full-width-image"
          src="/images/about/ludobox-box-web.jpg"
          alt="Ludobox Box Image"
          />
        <section id="printnplay">
          <img className="punchline"
            src="/images/ludobox-punchline1.png"
            alt="Punchline"
            />
          <h5>
            <span className="main">
              <FormattedMessage {...messages.printnplay.main} />
            </span>
            <br />
            <small>
              <span className="line1">
                <FormattedMessage {...messages.printnplay.line1} />
              </span>
              <br />
              <span className="line2">
                <FormattedMessage {...messages.printnplay.line2} />
              </span>
              <br />
              <span className="line3">
                <FormattedMessage {...messages.printnplay.line3} />
              </span>
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
        <section id="make">
          <h3 className="title">
            <FormattedMessage {...messages.make.title} />
          </h3>
          <div className="container">
            <h5>
              <span className='line1'>
                <FormattedMessage {...messages.make.line1} />
              </span>
              <br />
              <span className="line2">
                <FormattedMessage {...messages.make.line2} />
              </span>
            </h5>
          </div>
          <p className="doclink">
            <a href="https://hackmd.io/s/Skje3bygW" className="button" target="_blank">
              <FormattedMessage {...messages.make.button} />
            </a>
            <br />
          </p>
          <p className="links">
            <FormattedHTMLMessage {...messages.make.links} />
          </p>
        </section>
        <img className="full-width-image"
          src="/images/about/ludobox-workshop-kids.jpg"
          alt="Ludobox Kids Workshop"
          />
        <section id="contact" className="container" >
          <h3>Get in Touch</h3>
          <h5>
            <FormattedHTMLMessage {...messages.contact.wiki} />
            <br />
            <br />
            <span id="contact-text">Contact us at :</span> <a href="mailto:contact@ludobox.net">contact@ludobox.net</a>
          </h5>
        </section>
        <hr />
        <footer className="site-footer">
          <p className="support">
            <FormattedHTMLMessage {...messages.footer.credits} />
            <br />
            <small>
              <FormattedMessage {...messages.footer.sponsors} />
            </small>
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
