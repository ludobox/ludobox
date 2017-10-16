import React from 'react'

import './PageTitle.scss'

const PageTitle = ({ title, subtitle}) => (
  <header className="branding">
    <a href="/">
      <img src="/images/ludobox-logo-color2.png"/>
    </a>
    {
      title?
        <h1>{title}</h1>
      :
        null
    }
    {
      subtitle?
        <p className="subtitle">{subtitle}</p>
      :
        null
    }
  </header>
)


export default PageTitle
