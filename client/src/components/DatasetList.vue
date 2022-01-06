<template>
  <v-list
    outlined
    height="100%"
  >
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
import router from '@/router';
import { AxiosResponse } from 'axios';
import { RawLocation } from 'vue-router';

export default defineComponent({
  setup() {
    const datasets = ref([]);

    axiosInstance.get('/datasets/')
      .then((resp: AxiosResponse) => {
        datasets.value = resp.data.results;
      });

    function viewDataset(datasetId: string) {
      const route = {
        name: 'explore',
        params: { datasetId },
        query: {
          location: '',
        },
      } as RawLocation;

      router.push(route);
    }

    return {
      datasets,
      viewDataset,
    };
  },
});
</script>
