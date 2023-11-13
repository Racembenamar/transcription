<template>
    <div class="unauthorized-container">
      <h1>Access Denied</h1>
      <p>You must be logged in to view this page.</p>
      <button @click="redirectToLogin">Login</button>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      redirectToLogin() {
        this.$router.push('/login');
      }
    }
  };
  </script>
  
  <style>
  .unauthorized-container {
    /* Add styles for the container */
    text-align: center;
    padding: 50px;
  }
  
  .unauthorized-container button {
    /* Style for the login button */
    padding: 10px 20px;
    margin-top: 20px;
    cursor: pointer;
  }
  </style>
  