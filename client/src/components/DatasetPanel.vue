<script setup lang="ts">
import { ref, watch } from 'vue';
import { axiosInstance } from '@/api';
import FileList from './FileList.vue';

const props = defineProps({
  datasetId: {
    type: String,
    required: true,
  },
});

const properties = ref();

watch(() => props.datasetId, async () => {
  const { data } = await axiosInstance.get(`/datasets/${props.datasetId}/`);
  properties.value = data;
}, { immediate: true });

</script>

<template>
  <div>
    <span class="text-h6 justify-center d-flex">
      {{ properties.name }}
    </span>
    <v-divider />
    <file-list
      :dataset-id="datasetId"
      :raster-ids="properties.rasters"
      :mesh-ids="properties.meshes"
      :tiles3d-ids="properties.tiles3d"
      :fmv-ids="properties.fmvs"
    />
  </div>
</template>
