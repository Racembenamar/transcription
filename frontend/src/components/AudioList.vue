<template>
  <v-container>
    <v-btn @click="logout" color="red" class="logout-button">Logout</v-btn> <!-- Vuetify Button for Logout -->

    <h1>Available Audio Segments</h1>
    <v-btn color="primary" :to="{ name: 'AudioUpload' }">Upload Audio</v-btn> <!-- Vuetify Button for Upload -->

    <v-list>
      <v-list-item-group>
        <v-list-item v-for="audio in audioList" :key="audio.id">
          <v-list-item-content>
            Audio {{ audio.id }}
            <!-- Audio player for each audio -->
            <audio controls :src="audio.audioUrl"></audio>
            <v-btn v-if="isTranscriber" @click="goToTranscriptionForm(audio.id)" small color="success">Add Transcription</v-btn>
          </v-list-item-content>
          <v-divider></v-divider>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-container>
</template>




<script>
export default {
  data() {
    return {
      audioList: [],
      isTranscriber: false
    };
  },
  mounted() {
    // Retrieve user role information from local storage
    this.isTranscriber = localStorage.getItem('isTranscriber') === 'true';

    // Check for user authentication token
    const token = localStorage.getItem('userToken');
    if (!token) {
      // Redirect to unauthorized page if not logged in
      this.$router.push({ name: 'unauthorized' });
    } else {
      // Fetch audio segments if logged in
      this.fetchAudioSegments();
    }
  },
  methods: {
    fetchAudioSegments() {
      const token = localStorage.getItem('userToken');
      // Fetch audio segments from the server
      fetch('http://127.0.0.1:8000/api/audio_segments/?is_transcribed=false', {
        headers: {
          'Authorization': `Token ${token}`
        }
      })
      .then(response => response.json())
      .then(data => {
        this.audioList = data;
      })
      .catch(error => {
        console.error('Error fetching audio segments:', error);
      });
    },
    
    goToTranscriptionForm(audioId) {
      // Navigate to the transcription form
      this.$router.push({ name: 'TranscriptionForm', params: { audioId } });
    },
    
    logout() {
      // Clear the user token and redirect to the login page
      localStorage.removeItem('userToken');
      this.$router.push('/login');
    }
  }
};
</script>

<style>
.logout-button {
  padding: 10px;
  margin-bottom: 20px;
  background-color: #f44336;
  color: white;
  border: none;
  cursor: pointer;
}

/* Add additional styling as needed */
</style>
