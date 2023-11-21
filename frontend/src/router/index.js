import { createRouter, createWebHistory } from 'vue-router';
import AudioList from '../components/AudioList.vue';
import TranscriptionForm from '../components/TranscriptionForm.vue';
import UserLogin from '../components/UserLogin.vue';
import UserRegister from '../components/UserRegister.vue';
import Unauthorized from '../components/Unauthorized.vue';
import AudioUpload from '@/components/AudioUpload.vue';
import TranscribedAudioList from '@/components/TranscribedAudioList.vue';

const routes = [
  { path: '/', component: AudioList, meta: { requiresAuth: true } },
  { path: '/TranscriptionForm/:audioId', name: 'TranscriptionForm', component: TranscriptionForm, props: true, meta: { requiresAuth: true, requiresTranscribers: true } },
  { path: '/login/', component: UserLogin, name: 'login' },
  { path: '/register', component: UserRegister },
  { path: '/unauthorized', component: Unauthorized, name: 'unauthorized' },
  { path: '/upload', name: 'AudioUpload', component: AudioUpload, meta: { requiresAuth: true } },
  { path: '/transcribed-audios', component: TranscribedAudioList, name: 'TranscribedAudioList', meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('userToken');
  const is_transcriber = localStorage.getItem('is_transcriber') === 'true';

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!token) {
      next({ name: 'login' });
    } else {
      if (to.matched.some(record => record.meta.requiresTranscribers) && !is_transcriber) {
        next({ name: 'unauthorized' });
      } else {
        next();
      }
    }
  } else {
    next();
  }
});


export default router;
