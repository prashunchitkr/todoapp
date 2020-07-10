<template>
  <div>
    Login
    <p v-if="error">Incorrect Login Credentials</p>
    <form @submit.prevent="login">
      <input type="text" v-model="username" placeholder="username" required />
      <input type="password" v-model="password" placeholder="password" required />
      <input type="submit" />
    </form>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
      error: null
    };
  },
  methods: {
    login() {
      this.$store
        .dispatch("retrieveToken", {
          username: this.username,
          password: this.password
        })
        .then(() => this.$router.push("/"));
    }
  }
};
</script>
