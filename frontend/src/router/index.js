import { createRouter, createWebHistory } from 'vue-router';
import AudioList from '../components/AudioList.vue';
import TranscriptionForm from '../components/TranscriptionForm.vue';
import UserLogin from '../components/UserLogin.vue';
import UserRegister from '../components/UserRegister.vue';
import Unauthorized from '../components/Unauthorized.vue';
import AudioUpload from '@/components/AudioUpload.vue';

const routes = [
  { path: '/', component: AudioList },
  { path: '/TranscriptionForm/:audioId', name: 'TranscriptionForm', component: TranscriptionForm, props: true, meta: { requiresTranscribers: true } },
  { path: '/login/', component: UserLogin, name: 'login' },
  { path: '/register', component: UserRegister },
  { path: '/unauthorized', component: Unauthorized, name: 'unauthorized' },
  { path: '/upload', name: 'AudioUpload', component: AudioUpload}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('userToken');
  const isAudioUploader = localStorage.getItem('isAudioUploader') === 'true';
  const isTranscriber = localStorage.getItem('isTranscriber') === 'true'; 

  if (to.matched.some(record => record.meta.requiresAudioUploader)) {
    if (!token || !isAudioUploader) {
      next({ name: 'unauthorized' });
    } else {
      next();
    }
  } else if (to.matched.some(record => record.meta.requiresTranscribers)) {
    if (!token || !isTranscriber) {
      next({ name: 'unauthorized' });
    } else {
      next();
    }
  } else {
    next();
  }
});


export default router;
