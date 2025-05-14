import App from "./App.vue";
import { createApp } from "vue";
import router from "./router";
import { createPinia } from "pinia";

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";

import "./assets/main.css";

const app = createApp(App);

app.use(router);
app.use(createPinia());
app.mount("#app");
