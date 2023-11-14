<template>
  <div class="full-height-container">
    <div class="header">
      <v-btn @click="goBack" class="back-button">Back to List</v-btn>
      <v-btn @click="logout" class="logout-button">Logout</v-btn>
    </div>
    <h1>Upload Audio</h1>

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
  margin: 0;
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
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.upload-form {
  margin-top: 20px;
  width: 100%;
}

.logout-button, .back-button {
  margin: 0;
}

.center-text {
  text-align: center;
}

.spaced-columns th {
  padding-left: 20px;
  padding-right: 20px;
}
</style>
