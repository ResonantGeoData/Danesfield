import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import AlgorithmView from '@/views/AlgorithmView.vue';
import ExploreView from '@/views/ExploreView.vue';
import FocusView from '@/views/FocusView.vue';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
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
];

const router = new VueRouter({
  routes,
});

export default router;
