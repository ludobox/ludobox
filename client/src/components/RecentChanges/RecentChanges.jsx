import React from 'react'
import moment from 'moment'

// import History from '../History/History.jsx'
import APIClient from "../../api.js"


export default class RecentChanges extends React.Component {

  constructor(props) {
    super(props)
    this.api = new APIClient();
    this.state = {
      changes: []
    };
  }

  fetchRecentChanges() {
    this.api.getRecentChanges(changes => {
      this.setState({ changes })
    });
  }

  componentDidMount() {
    this.fetchRecentChanges()
  }

  render() {

    let {changes} = this.state
    console.log(changes);

    const events = changes.sort( (a,b) => b.event.ts - a.event.ts )
      .map( point => {
        let {title, slug, event} = point

        // parse date
        let d = moment
          .utc(event.ts*1000)
          .local()
          .fromNow();
          // .format('MMMM Do YYYY, h:mm:ss a');

        //


        return (
          <li key={event.id}>
            {event.type.toUpperCase()}D :
            <a href={`games/${slug}#${event.id}`}>
              {point.title}
            </a>
            {` ${d}`}
            {event.user ? ` by ${event.user} ` : null}
          </li>
        )
    })

    return (
      <div>
        <h3>Recent Changes</h3>
        <ul>
          {events}
        </ul>
      </div>
    )
  }
}
