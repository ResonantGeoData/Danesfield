import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import AlgorithmView from '@/views/AlgorithmView.vue';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: '/',
    component: AlgorithmView,
    props: true,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
