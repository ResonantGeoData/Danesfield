<script lang="ts">
import { uploadFiles } from '@/utils/upload';
import { defineComponent, ref, watch } from '@vue/composition-api';

export default defineComponent({
  name: 'UploadDialog',
  props: {
    single: {
      type: Boolean,
      default: false,
    },
  },
  setup(props, ctx) {
    const filesModel = ref<File[] | File>();
    const files = ref<File[]>([]);
    const uploading = ref(false);
    async function upload() {
      uploading.value = true;
      const uploadedFiles = await uploadFiles(files.value);
      uploading.value = false;

      ctx.emit('complete', uploadedFiles);

      // Cleanup
      files.value = [];
      filesModel.value = undefined;
    }

    // Set files to appropriate value
    watch(filesModel, (val) => {
      let returnVal = [] as File[];
      if (val instanceof File) {
        returnVal = [val];
      } else if (Array.isArray(val)) {
        returnVal = val;
      }

      files.value = returnVal;
    });

    return {
      files,
      filesModel,
      upload,
      uploading,
    };
  },
});
</script>

<template>
  <v-card>
    <v-card-title>
      Upload Data
    </v-card-title>
    <v-progress-linear
      v-if="uploading"
      indeterminate
    />
    <v-card-text>
      <v-file-input
        v-model="filesModel"
        :multiple="!single"
        clearable
      />
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn
        :disabled="!files.length"
        color="primary"
        @click="upload"
      >
        Upload
      </v-btn>
    </v-card-actions>
  </v-card>
</template>
