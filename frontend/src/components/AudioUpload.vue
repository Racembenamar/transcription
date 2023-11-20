<template>
  <v-container class="full-height-container">
    <div class="header">
      <v-btn @click="goBack" class="back-button">Back to List</v-btn>
      <v-btn @click="logout" class="logout-button">Logout</v-btn>
    </div>
    <h1 class="title">Upload Audio</h1>
    <br><br>
    <form @submit.prevent="uploadAudio" class="upload-form">
      <v-file-input
        label="File input"
        @change="handleFileChange"
        accept="audio/*"
        clearable
      ></v-file-input>
      <div class="button-container">
        <v-btn type="submit" color="primary">Upload</v-btn>
      </div>    </form>
    <p v-if="successMessage">{{ successMessage }}</p>
    <p v-if="errorMessage">{{ errorMessage }}</p>
    <v-snackbar v-model="showSnackbar">
      {{ snackbarMessage }}
    </v-snackbar>
  </v-container>

</template>

<script>
export default {
  data() {
    return {
      audioFile: null,
      successMessage: '',
      errorMessage: '',
      isAudioUploader: localStorage.getItem('isAudioUploader') === 'true',
      showSnackbar: false,
      snackbarMessage: '',

    };
  },
  methods: {
    handleFileChange(event) {
      this.audioFile = event.target.files[0];
    },

    uploadAudio() {
      if (!this.audioFile) {
        this.snackbarMessage = 'Please select an audio file to upload.';
        this.showSnackbar = true;
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
        this.snackbarMessage = 'Audio updated successfully !';
        this.showSnackbar = true;

      })
      .catch(error => {
        this.snackbarMessage = 'Faile to upload Audio';
        this.showSnackbar = true;
      });
    },
    
    logout() {
      localStorage.removeItem('userToken');
      this.$router.push('/login');
    },
    
    goBack() {
      this.$router.push('/');
    }
  }
};
</script>

<style>
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
  width: 100%;
}

.full-height-container {
  height: 100%;
  min-height: 100vh;
  width: 100%;
  margin: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.button-container {
    display: flex;
    justify-content: center;
    margin-top: 20px; 
  }

  .header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.upload-form {
  margin-top: 20px;
  width: 50%;
}

.logout-button {
  margin-right: 100px;
  margin-top: 80px;
}

.back-button {
  margin-left: 100px;
  margin-top: 80px;
}

.title {
  text-align: center;
  margin-top: 20px; 
}

.center-text {
  text-align: center;
}
</style>
