import Vue from "vue";
import Vuex from "vuex";
import { Axios } from "./api";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    todos: [],
    access_token: localStorage.getItem("access_token") || null,
  },
  getters: {
    loggedIn(state) {
      return state.access_token != null;
    },
  },
  mutations: {
    retrieveToken(state, token) {
      state.access_token = token;
    },
    retrieveTodos(state, todos) {
      state.todos = todos;
    },
    deleteTodo(state, id) {
      state.todos = state.todos.filter((todo) => todo.id != id);
    },
    addTodo(state, newTodo) {
      state.todos = [...state.todos, newTodo];
    },
    logout(state) {
      localStorage.removeItem("access_token");
      state.todos = [];
      state.access_token = null;
    },
  },
  actions: {
    retrieveToken(context, credentials) {
      const formData = new FormData();
      formData.append("username", credentials.username);
      formData.append("password", credentials.password);

      return new Promise((resolve, reject) => {
        Axios.post("/token", formData)
          .then((res) => {
            const token = res.data.access_token;
            context.commit("retrieveToken", token);
            localStorage.setItem("access_token", token);
            resolve(res);
          })
          .catch((e) => reject(e));
      });
    },
    retrieveTodos(context) {
      Axios.get("/todos")
        .then((res) => context.commit("retrieveTodos", res.data))
        .catch((err) => console.log(err));
    },
    deleteTodo(context, id) {
      Axios.delete(`/todos/${id}`);
      context.commit("deleteTodo", id);
    },
    addTodo(context, newTodo) {
      Axios.post("/todos", newTodo).then((res) =>
        context.commit("addTodo", res.data)
      );
    },
    updateTodo(context, todo) {
      Axios.put(`/todos/${todo.id}`, todo);
    },
  },
});

export default store;
