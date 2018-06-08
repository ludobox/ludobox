We use [`react-intl`](https://github.com/yahoo/react-intl) to bring internationalization (i18n) to Ludobox.

## How it works

* The default language is English
* Write all your messages directly inside the React component using the `defineMessages` function
* Run the `npm run extract-intl` to collect all the messages into a `i18n/**.json` file
* Handle the `i18n/**.json` file to a translator

## Example

**1. Add messages**

In `TranslatedComponent.jsx`

```jsx
import { FormattedMessage, defineMessages } from 'react-intl'
import React from 'react'

const messages = defineMessages({
    label: {
      id: 'translated.component.label',
      defaultMessage: 'Hello World',
      message: 'Hello World'
    },
  })

class TranslatedComponent extends React.Component {
  constructor(props) {
    super(props)
  }

  render() {
     render (
       <FormattedMessage {...messages.label} />
     )
  }
}
```

**2. Collect messages**

Run the command `npm run extract-intl` to create the JSON files with all the messages.  
This feature relies on the `[babel-plugin-react-intl](https://github.com/yahoo/babel-plugin-react-intl)` module.

result: `i18n/en.json`

```json
[
  {
    "id": "translated.component.label",
    "defaultMessage": "Hello World",
    "message": "Hello World"
  }
]
```

result: `i18n/fr.json`

```json
[
  {
    "id": "translated.component.label",
    "defaultMessage": "Hello World",
    "message": ""
  }
]
```

**3. Translate**

Just update the `i18n/fr.json`

```json
[
  {
    "id": "translated.component.label",
    "defaultMessage": "Hello World",
    "message": "Bonjour Monde"
  }
]
```

Et voilà !

## Contribute

Please feel free to add your own language by translating a file in `./i18n` folder.
