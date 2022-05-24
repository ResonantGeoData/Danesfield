import { createWebHashHistory, RouterOptions } from 'vue-router';
import AlgorithmView from '@/views/AlgorithmView.vue';
import ExploreView from '@/views/ExploreView.vue';
import FocusView from '@/views/FocusView.vue';

function makeOptions(): RouterOptions {
  return {
    history: createWebHashHistory(),
    routes: [
      {
        path: '/',
        redirect: 'explore',
      },
      {
        name: 'explore',
        path: '/explore',
        component: ExploreView,
        props: true,
      },
      {
        name: 'focus',
        path: '/focus/:datasetId?',
        component: FocusView,
        props: true,
      },
      {
        name: 'tasks',
        path: '/tasks',
        component: AlgorithmView,
        props: true,
      },
    ],
  };
}

export default makeOptions;
