<script setup lang="ts">
import { ref, watch } from 'vue';
import { uploadFiles } from '@/utils/upload';

defineProps({
  single: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['complete']);

const filesModel = ref<File[] | File>();
const files = ref<File[]>([]);
const uploading = ref(false);
async function upload() {
  uploading.value = true;
  const uploadedFiles = await uploadFiles(files.value);
  uploading.value = false;

  emit('complete', uploadedFiles);

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
