<template>
  <v-list
    outlined
    height="100%"
  >
    <span class="text-h6 justify-center d-flex">
      Datasets
    </span>
    <v-card
      v-for="dataset in datasets"
      :key="dataset.id"
      class="my-2"
      outlined
    >
      <v-list-item @click="viewDataset(dataset.id.toString())">
        <v-list-item-content>
          <v-list-item-title>{{ dataset.name }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-card>
  </v-list>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { AxiosResponse } from 'axios';
import { axiosInstance } from '@/api';
import router from '@/router';
import { Dataset } from '@/types';

const datasets = ref<Dataset[]>([]);

axiosInstance.get('/datasets/', { params: { include_input_datasets: false } })
  .then((resp: AxiosResponse) => {
    datasets.value = resp.data.results;
  });

function viewDataset(datasetId: string) {
  router.push({ name: 'focus', params: { datasetId } });
}
</script>
