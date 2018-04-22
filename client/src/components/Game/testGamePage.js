import { assert } from 'chai'
import {mapToList} from './GamePage.jsx'

console.log("haha")

describe('mapToList function', () => {
  it('should render an array as a text list', () => {
    assert.equal(mapToList([2,3]), "2 - 3")
  })

  it('should returns a single value if array items are identical', () => {
    assert.equal(mapToList([2,2]), "2")
  })

  it('should sort array items', () => {
    assert.equal(mapToList([2,1]), "1 - 2")
  })

  it('should filter out undefined values', () => {
    assert.equal(mapToList([undefined,undefined]), "")
  })
})
