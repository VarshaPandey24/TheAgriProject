import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// 1. Import your translation files
import enTranslation from './locales/en/translation.json';
import hiTranslation from './locales/hi/translation.json';

// 2. Define the resources
const resources = {
  en: {
    translation: enTranslation
  },
  hi: {
    translation: hiTranslation
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources, // 3. Add the resources object
    lng: 'en', // Default language
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false, // React already does escaping
    },
  });

export default i18n;