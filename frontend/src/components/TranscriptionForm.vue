<template>
  <div>
    <button @click="goBack" class="back-button">Back to List</button>
    <button @click="logout" class="logout-button">Logout</button>

    <h1>Transcribe Audio</h1>
    <audio v-if="audioUrl" controls :src="audioUrl"></audio>

    <v-form ref="form"> <!-- Add ref for form validation -->
      <v-container fluid>
        <v-textarea
          counter
          label="Transcription"
          :rules="textAreaRules"
          v-model="transcription"
        ></v-textarea>
      </v-container>
      <v-btn @click="validateAndSubmit" color="primary">Submit Transcription</v-btn>
    </v-form>

    <v-snackbar v-model="showSnackbar">
      {{ snackbarMessage }}
      <v-btn color="red" text @click="showSnackbar = false">Close</v-btn>
    </v-snackbar>

    <p v-if="processing">Processing...</p>
  </div>
</template>




<script>
export default {
  props: {
    audioId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      audioUrl: null,
      transcription: '',
      processing: false,
      rules: [v => v.length <= 1000 || 'Max 1000 characters'],
      showSnackbar: false,
      snackbarMessage: '',
      textAreaRules: [v => v.length <= 1000 || 'Max 1000 characters'], // Define your rules here

    };
  },
  mounted() {
  const audioId = parseInt(this.$route.params.audioId, 10);
  if (isNaN(audioId)) {
    console.error('Invalid audioId:', this.$route.params.audioId);
    // Optionally redirect to a different page if the audioId is invalid
  } else {
    const token = localStorage.getItem('userToken');
    if (!token) {
      this.$router.push({ name: 'unauthorized' });
    } else {
      this.fetchAudioData(audioId);
    }
  }
},



  methods: {
    fetchAudioData(audioId) {
    const token = localStorage.getItem('userToken'); // Retrieve the token from storage

    fetch(`http://127.0.0.1:8000/api/audio_segments/${audioId}`, {
      headers: {
        'Authorization': `Token ${token}`,  // Include the token in the request header
        'Content-Type': 'application/json',
      }
    })
    
  .then(response => {
    if (!response.ok) {
      // If the response is not OK, throw an error to be caught in the catch block
      throw new Error('Network response was not ok');
    }
    return response.json(); // Parse the JSON response
  })
  .then(data => {
    this.audioUrl = data.audio_file; // Set the audio URL
  })
  .catch(error => {
    console.error('Error fetching audio data:', error);
    // Handle errors here, such as displaying an error message
  });
  },

  validateAndSubmit() {
      if (this.$refs.form.validate()) { // Use ref to validate form
        this.submitTranscription();
      }
    },

    submitTranscription() {
      if (!this.audioId) {
      this.snackbarMessage = 'Audio ID is undefined.';
      this.showSnackbar = true;
      return;
    }
    this.processing = true;
    const token = localStorage.getItem('userToken');
    fetch(`http://127.0.0.1:8000/api/custom_audio_segments/${this.audioId}/`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ transcribed_text: this.transcription })
    })
    .then(response => {
      if (response.ok) {
        this.snackbarMessage = 'Transcription submitted successfully.';
        this.showSnackbar = true;
        this.transcription = '';
      } else {
        return response.json().then(data => {
          // Extracting the error message from the array
          this.snackbarMessage = data.transcribed_text.join(', ') || 'An error occurred while submitting the transcription.';
          this.showSnackbar = true;
        });
      }
    })
    .catch(error => {
      this.snackbarMessage = 'Error submitting transcription.';
      this.showSnackbar = true;
    })
    .finally(() => {
      this.processing = false;
    });
  },
    watch: {
  audioId(newVal, oldVal) {
    console.log('audioId changed from', oldVal, 'to', newVal);
  },
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
.logout-button {
  /* Styling for the logout button */
  padding: 10px;
  margin-bottom: 20px;
  background-color: #f44336;
  color: white;
  border: none;
  cursor: pointer;
}

.back-button {
  /* Styling for the back button */
  padding: 10px;
  margin: 10px 0;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

/* Add other CSS styling as needed */
</style>
