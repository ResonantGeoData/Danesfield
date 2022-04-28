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
    />
  </div>
</template>

<script lang="ts">
import { axiosInstance } from '@/api';
import { defineComponent, ref, watch } from '@vue/composition-api';
import FileList from './FileList.vue';

export default defineComponent({
  name: 'DatasetPanel',
  components: { FileList },
  props: {
    datasetId: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const properties = ref();

    watch(() => props.datasetId, async () => {
      const { data } = await axiosInstance.get(`/datasets/${props.datasetId}/`);
      properties.value = data;
    }, { immediate: true });

    return {
      properties,
    };
  },
});
</script>
