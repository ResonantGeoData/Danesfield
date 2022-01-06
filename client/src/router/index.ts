import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import AlgorithmView from '@/views/AlgorithmView.vue';
import Explore from '@/views/Explore.vue';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: '/',
    redirect: 'explore',
  },
  {
    name: 'explore',
    path: '/explore/:datasetId?',
    component: Explore,
    props: true,
  },
  {
    name: 'tasks',
    path: '/tasks',
    component: AlgorithmView,
    props: true,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
