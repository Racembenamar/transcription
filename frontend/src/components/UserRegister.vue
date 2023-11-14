<template>
  <v-container class="full-height-container">
    <v-row justify="center">
      <v-col cols="12" md="6" lg="4">
        <v-card class="pa-4">
          <v-form @submit.prevent="register">
            <v-text-field
              label="Username"
              v-model="username"
              outlined
              dense
              required
            ></v-text-field>

            <v-text-field
              label="Email"
              v-model="email"
              type="email"
              outlined
              dense
              required
            ></v-text-field>

            <v-text-field
              label="Password"
              v-model="password"
              type="password"
              outlined
              dense
              required
            ></v-text-field>

            <v-btn type="submit" color="primary" block>Register</v-btn>
            <v-btn @click="goToLogin" color="secondary" block class="mt-3">Back to Login</v-btn>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
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
          this.$router.push({ name: 'login' });
        
        })
        .catch((error) => {
          console.error('Registration failed:', error);
        });
      },
      goToLogin() {
      this.$router.push('/login'); 
    }
    }
    
  };
  </script>
  
<style>
.full-height-container {
  height: 100%;
  min-height: 100vh;
  width: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.justify-center {
  width: 100%;
}
</style>