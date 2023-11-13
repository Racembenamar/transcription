import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

// Vuetify
import 'vuetify/styles'; // Import Vuetify styles
import { createVuetify } from 'vuetify'; // Import Vuetify
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

const vuetify = createVuetify({
  components,
  directives,
});

const app = createApp(App);
app.use(vuetify);
app.use(router);
app.mount('#app');
