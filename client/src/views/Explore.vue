<template>
  <v-row
    style="height: 100%"
    no-gutters
  >
    <v-col cols="3">
      <dataset-list />
    </v-col>
    <v-col
      cols="9"
      class="d-flex justify-center align-center"
    >
      <CesiumViewer :footprints="footprints" />
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from '@vue/composition-api';
import { axiosInstance } from '@/api';
import DatasetList from '@/components/DatasetList.vue';
import CesiumViewer from '@/components/CesiumViewer.vue';
import DatasetPanel from '@/components/DatasetPanel.vue';

export default defineComponent({
  name: 'Explore',
  components: {
    DatasetList, CesiumViewer, DatasetPanel,
  },
  setup() {
    const footprints = ref({});

    onMounted(async () => {
      const { data } = await axiosInstance.get('/datasets/footprints/');
      footprints.value = data;
    });

    return {
      footprints,
    };
  },
});
</script>
