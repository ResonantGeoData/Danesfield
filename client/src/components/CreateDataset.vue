<script lang="ts">
import {
  computed, defineComponent, onMounted, ref,
} from '@vue/composition-api';

import { axiosInstance } from '@/api';
import { ChecksumFile } from '@/types';
import UploadDialog from '@/components/UploadDialog.vue';

const fileListHeaders = [
  { text: 'Name', value: 'name' },
  { text: 'Type (File/Url)', value: 'type' },
  { text: 'Uploaded', value: 'created' },
];

export default defineComponent({
  name: 'CreateDataset',
  components: {
    UploadDialog,
  },
  setup(props, ctx) {
    // Form datafileList
    const name = ref('');
    const files = ref<ChecksumFile[]>([]);
    const allFieldsValid = computed(() => name.value && files.value.length);

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

    const uploadDialogOpen = ref(false);
    async function filesUploaded() {
      uploadDialogOpen.value = false;
      fetchFileList();
    }

    // Intialize on mount
    onMounted(async () => {
      fetchFileList();
    });

    async function createDataset() {
      if (!allFieldsValid.value) {
        throw new Error('Attempted to create dataset with empty name and file list!');
      }

      const body = {
        name: name.value,
        files: files.value.map((f) => f.id),
      };

      const res = await axiosInstance.post('datasets/', body);
      if (res.status === 201) {
        // TODO
        // router.push({ name: 'algorithm', params: { id: res.data.id.toString() } });

        ctx.emit('created', res.data);

        // Clear data
        name.value = '';
        files.value = [];
      }
    }

    return {
      name,
      files,
      fileList,
      fileListHeaders,
      fileListSearch,
      fileListLoading,
      uploadDialogOpen,
      filesUploaded,
      createDataset,
      allFieldsValid,
    };
  },
});
</script>

<template>
  <v-card>
    <v-card-title>
      Create a new Dataset
      <v-dialog
        v-model="uploadDialogOpen"
        width="60vw"
      >
        <template v-slot:activator="{ on }">
          <v-btn
            color="primary"
            class="mx-1"
            icon
            right
            v-on="on"
          >
            <v-icon>
              mdi-upload
            </v-icon>
          </v-btn>
        </template>
        <upload-dialog @complete="filesUploaded" />
      </v-dialog>
      <v-spacer />
      <v-btn
        class="mx-1"
        color="success"
        :disabled="!allFieldsValid"
        @click="createDataset"
      >
        Create
        <v-icon right>
          mdi-plus
        </v-icon>
      </v-btn>
    </v-card-title>
    <v-card-text>
      <v-text-field
        v-model="name"
        label="Dataset Name"
        solo
        :rules="[(val) => (!!val || 'This field is required')]"
      />

      <v-card-title class="px-1">
        Select Files

        <template v-if="files.length">
          ({{ files.length }} selected)
        </template>
      </v-card-title>
      <v-card outlined>
        <v-data-table
          v-model="files"
          :search="fileListSearch"
          :loading="fileListLoading"
          title="Files"
          :items="fileList"
          :headers="fileListHeaders"
          selectable-key="id"
          show-select
        >
          <template v-slot:top>
            <v-text-field
              v-model="fileListSearch"
              label="Search Files"
              class="mx-4"
              clearable
            />
          </template>

          <!-- eslint-disable-next-line vue/valid-v-slot -->
          <template v-slot:item.type="{ item }">
            {{ item.type === 1 ? 'File' : 'Url' }}
          </template>
        </v-data-table>
      </v-card>
    </v-card-text>
  </v-card>
</template>
