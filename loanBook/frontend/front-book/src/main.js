import './assets/main.css';
import { createApp } from 'vue';
import { createVuetify } from 'vuetify';
import App from './App.vue';
import router from './router';
import axios from 'axios';
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';
// Vuetify
import 'vuetify/styles';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

// Configuration de Axios
axios.defaults.baseURL = "http://127.0.0.1:8000";

// Options pour Toastification
const toastOptions = {
  position: "top-right",
  timeout: 5000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: true,
  hideProgressBar: false,
  closeButton: "button",
  icon: true,
  rtl: false
};

// Créer une instance de Vuetify
const vuetify = createVuetify({
  components,
  directives,
});

// Créer une instance de l'application Vue
const app = createApp(App);

// Utiliser les plugins et le routeur
app.use(router);
app.use(Toast, toastOptions);
app.use(vuetify);

// Monter l'application
app.mount('#app');
