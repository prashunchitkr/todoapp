<template>
  <header class="header">
    <h1>TodoList</h1>
    <div class="nav" id="nav">
      <router-link to="/">Home</router-link>|
      <router-link to="/about">About</router-link>|
      <button v-if="loggedIn" @click="logout">Logout</button>
      <router-link v-else to="/login">Login</router-link>
    </div>
  </header>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "Header",
  methods: {
    logout() {
      this.$store.commit("logout");
      this.$router.push("/login");
    }
  },
  computed: mapState({
    loggedIn() {
      return this.$store.getters.loggedIn;
    }
  })
};
</script>

<style scoped>
.header {
  background: #333;
  color: #fff;
  text-align: center;
  padding: 10px;
}

.header a {
  color: #fff;
  padding-right: 5px;
}
</style>
