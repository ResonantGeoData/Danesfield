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
      <v-list-item @click="viewDataset(dataset.id)">
        <v-list-item-content>
          <v-list-item-title>{{ dataset.name }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-card>
  </v-list>
</template>

<script lang="ts">
import { defineComponent, ref } from '@vue/composition-api';
import { axiosInstance } from '@/api';
import { AxiosResponse } from 'axios';

export default defineComponent({
  setup() {
    const datasets = ref([]);

    axiosInstance.get('/datasets/')
      .then((resp: AxiosResponse) => {
        datasets.value = resp.data.results;
      });

    function viewDataset(datasetId: string) {
      // TODO: implement focus view for dataset
    }

    return {
      datasets,
      viewDataset,
    };
  },
});
</script>
