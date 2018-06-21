import { addLocaleData } from 'react-intl'
import en from 'react-intl/locale-data/en'
import fr from 'react-intl/locale-data/fr'

import enUSMessages from '../i18n/en'
import frFRMessages from '../i18n/fr'

addLocaleData([...en, ...fr])

export const appLocales = [
  'en',
  'fr',
]

export const formatTranslationMessages = (messages) => {
  const formattedMessages = {}
  for (const message of messages) {
    formattedMessages[message.id] = message.message || message.defaultMessage
  }
  return formattedMessages
}

export const messages = {
  'en' : formatTranslationMessages(enUSMessages),
  'fr' : formatTranslationMessages(frFRMessages)
}
