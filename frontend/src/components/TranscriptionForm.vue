<template>
  <div class="full-height-container">
    <div class="header">
      <v-btn @click="goBack" class="back-button">Back to List</v-btn>
      <h1>Transcribe Audio</h1>
      <v-btn @click="logout" class="logout-button">Logout</v-btn>
    </div>
    
    <audio v-if="audioUrl" controls :src="audioUrl"></audio>

    <v-form ref="form" class="transcription-form">
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
      textAreaRules: [v => v.length <= 1000 || 'Max 1000 characters'], 

    };
  },
  mounted() {
  const audioId = parseInt(this.$route.params.audioId, 10);
  if (isNaN(audioId)) {
    console.error('Invalid audioId:', this.$route.params.audioId);
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
    const token = localStorage.getItem('userToken'); 

    fetch(`http://127.0.0.1:8000/api/audio_segments/${audioId}`, {
      headers: {
        'Authorization': `Token ${token}`,  
        'Content-Type': 'application/json',
      }
    })
    
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json(); 
  })
  .then(data => {
    this.audioUrl = data.audio_file; 
  })
  .catch(error => {
    console.error('Error fetching audio data:', error);
  });
  },

  validateAndSubmit() {
      if (this.$refs.form.validate()) { 
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
      localStorage.removeItem('userToken');  
      this.$router.push('/login');           
    },
    goBack() {
      this.$router.push('/'); 
    },

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
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.transcription-form {
  margin-top: 20px;
  width: 100%;
}

.logout-button {
  margin: 0;
}

.back-button {
  margin: 0;
}

.spaced-columns td {
  padding-left: 20px;
  padding-right: 20px;
}
</style>