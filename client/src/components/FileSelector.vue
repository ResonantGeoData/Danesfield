<script setup lang="ts">
import {
  onMounted, ref, watch, PropType,
} from 'vue';

import { axiosInstance } from '@/api';
import { ChecksumFile } from '@/types';

const fileListHeaders = [
  { text: 'Name', value: 'name' },
  { text: 'Type (File/Url)', value: 'type' },
  { text: 'Uploaded', value: 'created' },
];

const props = defineProps({
  single: {
    type: Boolean,
    default: false,
  },
  value: {
    type: Array as PropType<ChecksumFile[]>,
    required: true,
  },
});

const emit = defineEmits(['input']);

// Form datafileList
const fileList = ref<ChecksumFile[]>([]);
const fileListSearch = ref('');
const fileListLoading = ref(false);
async function fetchFileList() {
  fileListLoading.value = true;

  try {
    // TODO: Deal with server pagination
    const datasetsRes = await axiosInstance.get('rgd/checksum_file', { params: { limit: 1000 } });
    fileList.value = datasetsRes.data.results;
  } catch (error) {
    // TODO: Handle
  }

  fileListLoading.value = false;
}

// Intialize on mount
onMounted(async () => {
  fetchFileList();
});

// Emit event anytime selected files are changed
const selectedFiles = ref<ChecksumFile[]>([]);
watch(selectedFiles, (val) => {
  emit('input', val);
});

// Watch for value set
watch(() => props.value, (val) => {
  selectedFiles.value = val || [];
});

</script>

<template>
  <v-data-table
    v-model="selectedFiles"
    :search="fileListSearch"
    :loading="fileListLoading"
    title="Files"
    :items="fileList"
    :headers="fileListHeaders"
    selectable-key="id"
    show-select
    :single-select="single"
  >
    <template #top>
      <v-text-field
        v-model="fileListSearch"
        label="Search Files"
        class="mx-4"
        clearable
      />
    </template>

    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #item.type="{ item }">
      {{ item.type === 1 ? 'File' : 'Url' }}
    </template>
  </v-data-table>
</template>
