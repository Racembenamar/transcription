<template>
  <v-container class="full-height-container">
    <v-row justify="center">
      <v-col cols="12" md="6" lg="4">
        <v-card class="pa-4">
          <v-form @submit.prevent="login">
            <v-text-field
              label="Username"
              v-model="username"
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

            <v-btn type="submit" color="primary" block>Login</v-btn>
            <v-btn @click="goToRegister" color="secondary" block class="mt-3">Register</v-btn>

          </v-form>
          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
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
      password: '',
      errorMessage: '',
      isAudioUploader: localStorage.getItem('isAudioUploader') === 'true'
    };
  },
  methods: {
    login() {
      fetch('http://127.0.0.1:8000/api/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password
        })
      })
      .then(response => {
        return response.json();
      })
      .then(data => {
        if (data.token) {
            localStorage.setItem('userToken', data.token);
            localStorage.setItem('isTranscriber', data.is_transcriber); 
            localStorage.setItem('isAudioUploader', data.is_audio_uploader); 

            this.$router.push('/');
        } else {
            this.errorMessage = 'Login failed: ' + (data.error || 'Unknown error');
        }
      })
      .catch(error => {
        console.error('Login error:', error);
        this.errorMessage = 'Login error: ' + error.message;
      });
    },
    goToRegister() {
      this.$router.push('/register'); 
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
.error-message {
  color: red;
  text-align: center;
  margin-top: 10px;
}
</style>