import React from 'react'
import './about.scss'
import PageTitle from '../PageTitle/PageTitle.jsx'
import { FormattedMessage, FormattedHTMLMessage, defineMessages } from 'react-intl'

const messages = defineMessages({
    description: {
      id: 'about.description',
      defaultMessage: 'Ludobox is an open collection of Print’n Play games which are regrouped on an online plateform with many files, instructions and recipes to create and built games yourself.'
    },
    descriptionSmall: {
      id: 'about.description.small',
      defaultMessage: 'Each box contains dozens of digital files and instructions to make your own games and turns any place into a game library.'
    },
    printnplayMain : {
      id : 'about.printnplay.main',
      defaultMessage: "Print'n play are games that you can make by yourself."
    },
    printnplayLine1: {
      id : 'about.printnplyt.line1',
      defaultMessage: "From a card game in PDF using a printer and scissors"
    },
    printnplayLine2: {
      id : 'about.printnplay.line2',
      defaultMessage: "to a board game accessing a 3D printer to reproduce tokens,"
    },
    printnplayLine3: {
      id : 'about.printnplay.line3',
      defaultMessage: "Ludobox invites to materialize & craft digital files."
    },
    makeTitle : {
      id: 'about.make.title',
      defaultMessage: 'Make your own Box'
    },
    makeLine1: {
      id : 'about.make.line2',
      defaultMessage: "You can build your own box from scratch"
    },
    makeLine2: {
      id : 'about.make.line3',
      defaultMessage: "and directly download games from our online collection."
    },
    makeButton : {
      id : 'about.make.button',
      defaultMessage: "Create your own"
    },
    makeLinks : {
      id : 'about.make.links',
      defaultMessage: 'Check <a href="https://github.com/ludobox/ludobox">the code</a> or read <a href="https://wiki.ludobox.net">the docs</a>'
    },
    contactWiki : {
      id :'about.contact.wiki',
      defaultMessage : 'You’d like to contribute to Ludobox platform ? Visit the <a href="https://wiki.ludobox.net">wiki</a>.'
    },
    contactEmail : {
      id :'about.contact.email',
      defaultMessage : '<span id="contact-text">Contact us at :</span> <a href="mailto:contact@ludobox.net">contact@ludobox.net</a>'
    },
    contactCatalogue : {
      id :'about.contact.catalogue',
      defaultMessage : 'For more info, you can also consult our '
    },
    contactCatalogueLink : {
      id :'about.contact.catalogueLink',
      defaultMessage : 'catalogue <small>(French only)</small>.'
    },
    footerCredits : {
      id: 'about.footer.credits',
      defaultMessage: 'This project is powered by <a className="no-external" href="http://dcalk.org" target="_blank"><b>DCALK</b>.</a>'
    },
    footerSponsors : {
      id: 'about.footer.sponsors',
      defaultMessage: 'It was made possible with the support of'
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
              <FormattedMessage {...messages.printnplayMain} />
            </span>
            <br />
            <small>
              <span className="line1">
                <FormattedMessage {...messages.printnplayLine1} />
              </span>
              <br />
              <span className="line2">
                <FormattedMessage {...messages.printnplayLine2} />
              </span>
              <br />
              <span className="line3">
                <FormattedMessage {...messages.printnplayLine3} />
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
            <FormattedMessage {...messages.makeTitle} />
          </h3>
          <div className="container">
            <h5>
              <span className='line1'>
                <FormattedMessage {...messages.makeLine1} />
              </span>
              <br />
              <span className="line2">
                <FormattedMessage {...messages.makeLine2} />
              </span>
            </h5>
          </div>
          <p className="doclink">
            <a href="https://hackmd.io/s/Skje3bygW" className="button" target="_blank">
              <FormattedMessage {...messages.makeButton} />
            </a>
            <br />
          </p>
          <p className="links">
            <FormattedHTMLMessage {...messages.makeLinks} />
          </p>
        </section>
        <img className="full-width-image"
          src="/images/about/ludobox-workshop-kids.jpg"
          alt="Ludobox Kids Workshop"
          />
        <section id="contact" className="container" >
          <h3>Get in Touch</h3>
          <h5>
            <FormattedHTMLMessage {...messages.contactWiki} />
            <br />
            <FormattedHTMLMessage {...messages.contactCatalogue} /> <a href="https://wiki.ludobox.net/files/CatalogueLudobox.pdf">
              <FormattedHTMLMessage {...messages.contactCatalogueLink} />
            </a>
            <br />
            <br />
            <FormattedHTMLMessage {...messages.contactEmail} />
          </h5>
        </section>
        <hr />
        <footer className="site-footer">
          <p className="support">
            <FormattedHTMLMessage {...messages.footerCredits} />
            <br />
            <small>
              <FormattedMessage {...messages.footerSponsors} />
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
