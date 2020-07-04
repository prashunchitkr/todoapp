<template>
  <div>
    <AddTodo v-on:add-todo="newTodo => this.$emit('add-todo', newTodo)" />
    <div v-for="todo in todos" v-bind:key="todo.id">
      <TodoItem v-bind:todo="todo" v-on:del-todo="$emit('del-todo', todo.id)" />
    </div>
  </div>
</template>

<script>
import TodoItem from "./TodoItem";
import AddTodo from "./AddTodo";

export default {
  name: "Todos",
  props: ["todos"],
  components: {
    TodoItem,
    AddTodo
  }
};
</script>

<style scoped>
</style>
