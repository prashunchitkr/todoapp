<template>
  <div class="home">
    <Todos />
  </div>
</template>

<script>
import Todos from "../components/Todos";

export default {
  name: "Home",
  components: {
    Todos
  },
  created() {
    this.$store.dispatch("retrieveTodos");
  }
};
</script>

