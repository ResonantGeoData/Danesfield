<template>
  <v-row
    style="height: 100%"
    no-gutters
  >
    <v-col cols="3">
      <file-browser
        v-if="datasetId"
        :dataset-id="datasetId"
      />
      <dataset-list v-else />
    </v-col>
    <v-col
      cols="9"
      class="d-flex justify-center align-center"
    >
      <iframe
        v-if="iframeSrc"
        :src="iframeSrc"
        height="100%"
        width="100%"
      />
      <template v-else>
        Select a file to view.
      </template>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { computed, defineComponent, watch } from '@vue/composition-api';
import { axiosInstance } from '@/api';
import { openFile, setOpenFile } from '@/store';
import DatasetList from '@/components/DatasetList.vue';
import FileBrowser from '@/components/FileBrowser.vue';

export default defineComponent({
  name: 'Explore',
  components: { DatasetList, FileBrowser },
  props: {
    datasetId: {
      type: Number,
      required: false,
    },
  },
  setup(props) {
    const iframeSrc = computed(() => (openFile.value ? `${axiosInstance.defaults.baseURL}datasets/${props.datasetId}/viewer/${openFile.value}` : undefined));

    // Unset open file if the user navigates to a different URL
    watch(() => props.datasetId, () => setOpenFile(''));

    return {
      iframeSrc,
    };
  },
});
</script>
