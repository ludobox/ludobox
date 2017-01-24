/* eslint-env mocha */
import React from 'react'
import { shallow } from 'enzyme'
import { assert } from 'chai'

import Home from './Home.jsx'

describe('<Home />', () => {
  it('should say hello', () => {
    const home = shallow(<Home />);
    const title = home.find('h3');
    assert.match(title.text(), /^Hello/)
  })
})
