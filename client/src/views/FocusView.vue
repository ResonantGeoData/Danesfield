<script setup lang="ts">
import CesiumViewer from '@/components/CesiumViewer.vue';
import DatasetPanel from '@/components/DatasetPanel.vue';

defineProps({
  datasetId: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <v-row
    style="height: 100%"
    no-gutters
  >
    <v-col cols="3">
      <DatasetPanel :dataset-id="datasetId" />
    </v-col>
    <v-col
      cols="9"
      class="d-flex justify-center"
      style="height: 100%;"
    >
      <CesiumViewer />
    </v-col>
  </v-row>
</template>
