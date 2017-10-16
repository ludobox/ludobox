import React from 'react'

import PageTitle from '../PageTitle/PageTitle.jsx'

export default class AboutPage extends React.Component {

  render() {

    return (
      <div>
        <PageTitle title="About"/>
        <p>DIGITAL TOY LIBRARY : an offline device to share games released under free licenses</p>
        <p><strong>In 2014, Dcalk started to develop the idea of a Digital Toy Library &#8211; following the PirateBox and LibraryBox successful initiatives allowing to share free digital content through an offline network – to gather free-licensed games&#8230; Yes it exists (!) and that&rsquo;s exactly to support this practice and give visibility to these creations that we wish to do so.</strong></p>
        <p>The LudoBox project has emerged from the nomadic mediation formula tested in the last 3 years : the Dark Toy Library (a pop-up collection of indie board games carrying critical content, some of them released under CC licence) and the Mobile Digital Fabrique (a foldable 3D printer allowing us to organize Print Parties to make on site 3D printed open source board games), the Digital Toy Library or LudoBox facilitates, through an autonomous wifi router, to gather and access:</p>
        <ul>
        <li>digital files ready-to-print containing rules and games&rsquo;elements: role playing, urban game, card game to be cut, board to be made, etc.)</li>
        <li>files in .stl format (checkers, plates, tiles) for 3D printing</li>
        <li>game storage box pattern (cardboard or organic materials for laser cutter)</li>
        <li>pedagogical resources (tutorials and manuals on tools or free software, documentation / methodology to run game design workshops, etc.)</li>
        <li>publications on game design, free culture, DIY (essays, articles, e-books, etc)</li>
        </ul>
        <p>End of 2015, we wish to deliver a first version of Ludobox with installation packages and tutorial, and a wiki gathering games, resources, publications to install its own offline collection. Several stages, many tasks&#8230; an open playground !</p>
        <p>To know more about the project, download the file : <a href="https://leschiensdelenfer.files.wordpress.com/2015/03/ludobox_en.pdf">LudoBox_en</a></p>
        <p style={{textAlign:"center"}}><strong>You like the LudoBox&rsquo;s idea ? </strong><br />
        <strong> You want to contribute, welcome us or recomend resources, , feel free to contact us: </strong>info@dcalk.org</p>
      </div>
    )
  }
}
