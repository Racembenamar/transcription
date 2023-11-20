<template>
  <v-container class="full-height-container">
    <div class="header">
      <v-btn @click="goBack" class="back-button">Back to List</v-btn>
      <v-btn @click="logout" class="logout-button">Logout</v-btn>
    </div>
    <h1 class="title">Transcribed Audios</h1>
    <br><br>
    <table class="center-text spaced-columns">
      <thead>
        <tr>
          <th class="center-text">Audio ID</th>
          <th class="center-text">Player</th>
          <th class="center-text">Transcribed Text</th>
          <th class="center-text">Transcriber</th>
        </tr>
      </thead>
      <tbody class="center-text">
        <tr v-for="audio in transcribedAudios" :key="audio.id">
          <td>{{ audio.id }}</td>
          <td><audio controls :src="audio.audio_file"></audio></td>
          <td>{{ audio.transcribed_text }}</td>
          <td>{{ audio.transcribed_by_username }}</td>
        </tr>
      </tbody>
    </table>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      transcribedAudios: [],
      baseUrl: 'http://127.0.0.1:8000'
    };
  },
  mounted() {
    this.fetchTranscribedAudios();
  },
  methods: {
    fetchTranscribedAudios() {
      const token = localStorage.getItem('userToken');
      fetch(`${this.baseUrl}/api/transcribed_audios/`, {
        headers: {
          'Authorization': `Token ${token}`,
        },
      })
      .then(response => response.json())
      .then(data => {
        this.transcribedAudios = data.map(audio => {
          return {
            ...audio,
            audio_file: this.baseUrl + audio.audio_file
          };
        });
      })
      .catch(error => {
        console.error('Error fetching transcribed audios:', error);
      });
    },

    logout() {
      localStorage.removeItem('userToken');
      this.$router.push('/login');
    },
    
    goBack() {
      this.$router.go(-1);
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
  justify-content: space-between;
  align-items: center;
}

.logout-button {
  margin-left: auto;
}

.spaced-columns th {
  padding-left: 40px;
  padding-right: 40px;
}

.title {
  text-align: center;
  margin-top: 20px; 
}

</style>
