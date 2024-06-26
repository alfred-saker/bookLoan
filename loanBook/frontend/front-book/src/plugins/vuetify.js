import { createVuetify } from 'vuetify';
import 'vuetify/styles';
import '@mdi/font/css/materialdesignicons.css'; // Importer les styles des icônes MDI

// Importer des icônes
import { aliases, mdi } from 'vuetify/iconsets/mdi';

const vuetify = createVuetify({
  icons: {
    defaultSet: 'mdi', // Utiliser le set d'icônes MDI par défaut
    aliases,
    sets: {
      mdi,
    },
  },
  ssr: true,
  theme: {
    themes: {
      light: {
        primary: '#1E88E5',
        secondary: '#FFEBB7',
        accent: '#4CAF50',
        background: '#F5F5F5',
        text: '#424242',
        error: '#FF5252',
        info: '#2196F3',
        success: '#4CAF50',
        warning: '#FFC107',
      },
    },
  },
});

export default vuetify;
