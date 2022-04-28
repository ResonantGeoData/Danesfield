<template>
  <v-row
    style="height: 100%"
    no-gutters
  >
    <v-col cols="3">
      <dataset-panel :dataset-id="datasetId" />
    </v-col>
    <v-col
      cols="9"
      class="d-flex justify-center align-center"
    >
      <CesiumViewer />
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api';
import DatasetList from '@/components/DatasetList.vue';
import CesiumViewer from '@/components/CesiumViewer.vue';
import DatasetPanel from '@/components/DatasetPanel.vue';

export default defineComponent({
  name: 'Focus',
  components: {
    DatasetList, CesiumViewer, DatasetPanel,
  },
  props: {
    datasetId: {
      type: String,
      required: false,
    },
  },
});
</script>
