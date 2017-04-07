/* eslint-env mocha */
import React from 'react'
import { shallow } from 'enzyme'
import { assert } from 'chai'

import Home from './Home.jsx'

const config = {
  name : "My Test Box"
}

describe('<Home />', () => {
  it('should say Hello', () => {
    const home = shallow(<Home config={config}/>);
    const title = home.find('h3');
    assert.match(title.text(), /^Hello/)
  })

  it('should display the name of the box', () => {
    const home = shallow(<Home config={config}/>);
    const welcome = home.find('.welcome');
    assert.include(welcome.text(), config.name)
  })
})
