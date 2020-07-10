<template>
  <div>
    <AddTodo />
    <div v-for="todo in todos" v-bind:key="todo.id">
      <TodoItem v-bind:todo="todo" />
    </div>
  </div>
</template>

<script>
import TodoItem from "./TodoItem";
import AddTodo from "./AddTodo";
import { mapState } from "vuex";

export default {
  name: "Todos",
  components: {
    TodoItem,
    AddTodo
  },
  computed: mapState(["todos"])
};
</script>

<style scoped>
</style>
