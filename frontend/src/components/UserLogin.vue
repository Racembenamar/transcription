<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="login">
      <input type="text" v-model="username" placeholder="Username">
      <input type="password" v-model="password" placeholder="Password">
      <button type="submit">Login</button>
    </form>
    <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
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
            localStorage.setItem('isTranscriber', data.is_transcriber); // Store the transcriber status
            localStorage.setItem('isAudioUploader', data.is_audio_uploader); // Store the user role

            this.$router.push('/');
        } else {
            this.errorMessage = 'Login failed: ' + (data.error || 'Unknown error');
        }
      })
      .catch(error => {
        console.error('Login error:', error);
        this.errorMessage = 'Login error: ' + error.message;
      });
    }
  }
};
</script>
