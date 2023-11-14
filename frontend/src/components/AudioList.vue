<template>
  <v-container class="full-height-container">
    <div class="header">
      <h1>Available Audio Segments</h1>
      <v-btn @click="logout"  class="logout-button">Logout</v-btn>
    </div>
    <br> 
    <br> 
<br> 

    <v-btn  :to="{ name: 'AudioUpload' }">Upload Audio</v-btn>
<br> <br> 
<br> 

    <table class="center-text">
      <thead>
        <tr>
          <th class="center-text">Audio Name</th>
          <th class="center-text">Player</th>
          <th class="center-text" v-if="isTranscriber">Actions</th>
        </tr>
      </thead>
      <tbody class="center-text">
        <tr v-for="(audio, index) in audioList" :key="audio.id">
          <td>Audio {{ index + 1 }}</td>
          <td><audio controls :src="audio.audio_file"></audio></td>
          <td v-if="isTranscriber">
            <v-btn @click="goToTranscriptionForm(audio.id)" small>Edit Transcription</v-btn>
          </td>
        </tr>
      </tbody>
    </table>
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
    this.isTranscriber = localStorage.getItem('isTranscriber') === 'true';
    this.fetchAudioSegments(); 
  },
  methods: {
    fetchAudioSegments() {
      const token = localStorage.getItem('userToken');
      fetch('http://127.0.0.1:8000/api/audio_segments/?is_transcribed=false', {
        headers: {
          'Authorization': `Token ${token}`
        }
      })
      .then(response => response.json())
      .then(data => {
        this.audioList = data.map((item, index) => {
          return { ...item, name: `Audio ${index + 1}` }; 
        });
      })
      .catch(error => {
        console.error('Error fetching audio segments:', error);
      });
    },
    goToTranscriptionForm(audioId) {
      this.$router.push({ name: 'TranscriptionForm', params: { audioId } });
    },
    logout() {
      localStorage.removeItem('userToken');
      this.$router.push('/login');
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
  padding: 0;
}

.center-text {
  text-align: center;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logout-button {
  margin-left: auto;
}


</style>
