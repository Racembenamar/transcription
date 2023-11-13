<template>
    <div>
      <h1>Register</h1>
      <form @submit.prevent="register">
        <input type="text" v-model="username" placeholder="Username">
        <input type="email" v-model="email" placeholder="Email">
        <input type="password" v-model="password" placeholder="Password">
        <button type="submit">Register</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: '',
        email: '',
        password: ''
      };
    },
    methods: {
      register() {
        const userData = {
          username: this.username,
          email: this.email,
          password: this.password
        };
  
        fetch('http://127.0.0.1:8000/api/register/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(userData)
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          console.log(data); // Handle the response data
          this.$router.push({ name: 'login' });
        
        })
        .catch((error) => {
          console.error('Registration failed:', error);
          // Handle errors here, such as displaying a notification to the user
        });
      }
    }
  };
  </script>
  