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
    assert.match(title.text(), /^Welcome/)
  })

  it('should display the name of the box', () => {
    const home = shallow(<Home config={config}/>);
    const welcome = home.find('.welcome');
    assert.include(welcome.text(), config.name)
  })

  it('should show `download` when web_server_url is not null', () => {
    const home = shallow(<Home config={
      {
        config : {
          ...config,
          web_server_url : "http://box.ludobox.net"
        }
      }
    }/>);
    const download = home.find('a[href="/download"]');
    assert.equal(download.length, 1);
  })

  it('should hide `download` when web_server_url is null', () => {
    const home = shallow(<Home config={
      {
        config : {
          ...config,
          web_server_url : null
        }
      }
    }/>);
    const download = home.find('a[href="/download"]');
    assert.equal(download.length, 0);
  })
})
