import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import { Axios } from "./api";

Vue.config.productionTip = false;

Vue.prototype.$http = Axios;

Axios.interceptors.request.use(
  (config) => {
    const token = store.state.access_token;
    if (token) {
      config.headers.common["Authorization"] = `Bearer ${token}`;
    }
    config.headers.common["Access-Control-Allow-Origin"] = "*";
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!store.getters.loggedIn) {
      next({
        path: "/login",
      });
    } else {
      next();
    }
  } else if (to.matched.some((record) => record.meta.requiresVisitor)) {
    if (store.getters.loggedIn) {
      next({
        path: "/",
      });
    } else {
      next();
    }
  } else {
    next();
  }
});

new Vue({
  router,
  render: (h) => h(App),
  store: store,
}).$mount("#app");
