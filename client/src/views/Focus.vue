<template>
  <v-row
    style="height: 100%"
    no-gutters
  >
    <v-col cols="3">
      <file-browser />
    </v-col>
    <v-col cols="9">
      <!-- TODO: put iframe to RGD server-rendered pages here -->
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api';
import FileBrowser from '@/components/FileBrowser.vue';

export default defineComponent({
  name: 'Focus',
  components: { FileBrowser },
  props: {
    // datasetId: {
    //   type: String,
    //   required: true,
    // },
  },
  setup() {
    return {
    };
  },
});
</script>
