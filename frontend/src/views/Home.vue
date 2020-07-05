<template>
  <div v-if="loading">
    <h3>Loading...</h3>
  </div>
  <div class="home" v-else>
    <Todos v-bind:todos="todos" v-on:del-todo="deleteTodo" v-on:add-todo="addTodo" />
  </div>
</template>

<script>
import Todos from "../components/Todos";
import { Axios } from "../Api";

export default {
  name: "Home",
  components: {
    Todos
  },
  data() {
    return {
      todos: [],
      loading: true
    };
  },
  methods: {
    deleteTodo(id) {
      Axios.delete(`/todos/${id}`).catch(e => console.log(e));
      this.todos = this.todos.filter(todo => todo.id != id);
    },
    addTodo(newTodo) {
      Axios.post("/todos", newTodo)
        .then(res => (this.todos = [...this.todos, res.data]))
        .catch(e => console.log(e));
    }
  },
  created() {
    Axios.get("/todos")
      .then(res => (this.todos = res.data))
      .catch(err => console.log(err))
      .finally(() => (this.loading = false));
  }
};
</script>

