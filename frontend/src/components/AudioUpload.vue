<template>
  <div>
    <v-btn @click="goBack" class="back-button">Back to List</v-btn> <!-- Back Button -->

    <v-btn @click="logout" class="logout-button">Logout</v-btn> <!-- Logout Button -->

    <h1>Upload Audio File</h1>
    <form @submit.prevent="uploadAudio">
      <v-file-input
        label="File input"
        @change="handleFileChange"
        accept="audio/*"
        clearable
      ></v-file-input>
      <v-btn type="submit" color="primary">Upload</v-btn>
    </form>
    <p v-if="successMessage">{{ successMessage }}</p>
    <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>

  
  <script>
  export default {
    data() {
      return {
        audioFile: null,
        successMessage: '',
        errorMessage: '',
        isAudioUploader: localStorage.getItem('isAudioUploader') === 'true'

      };
    },
    methods: {
      handleFileChange(event) {
        this.audioFile = event.target.files[0];
      },
      uploadAudio() {
      if (!this.audioFile) {
        this.errorMessage = 'Please select an audio file to upload.';
        return;
      }

      const formData = new FormData();
      formData.append('audio_file', this.audioFile);

      fetch('http://127.0.0.1:8000/api/audio_upload/', {
        method: 'POST',
        headers: {
          'Authorization': `Token ${localStorage.getItem('userToken')}`
        },
        body: formData
      })
      .then(response => {
        if (!response.ok) {
          return response.text().then(text => { throw new Error(text || 'Upload failed') });
        }
        return response.json();
      })
      .then(data => {
        this.successMessage = 'Audio file uploaded successfully!';
      })
      .catch(error => {
        console.error('Error:', error);
        this.errorMessage = `Upload error: ${error}`;
      });
    

      },
      logout() {
      localStorage.removeItem('userToken');  // Clear the token
      this.$router.push('/login');           // Redirect to the login page
    },
    goBack() {
      this.$router.push('/'); // Assuming the root path ('/') is your audio list
    },
    }
  };
  </script>
  
  <style>
  /* Add styles for your form, buttons, messages here */
  </style>
  