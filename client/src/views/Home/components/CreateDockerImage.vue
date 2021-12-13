<script lang="ts">
/* eslint-disable @typescript-eslint/camelcase */
import {
  computed, defineComponent, ref, watch,
} from '@vue/composition-api';

import { axiosInstance } from '@/api';
import FileSelector from '@/components/FileSelector.vue';
import UploadDialog from '@/components/UploadDialog.vue';
import { ChecksumFile } from '@/types';

interface DockerCreatePayload {
  name: string;
  image_file: number | null;
  image_id: string | null;
}

export default defineComponent({
  name: 'CreateDockerImage',
  components: {
    FileSelector,
    UploadDialog,
  },
  setup(props, ctx) {
    const name = ref('');
    const imageId = ref('');
    const imageFile = ref<ChecksumFile>();
    const createDisabled = computed(() => !(name.value && (imageId.value || imageFile.value)));

    async function createDockerImage() {
      if (createDisabled.value) {
        throw new Error('Attempted to create dataset with invalid args!');
      }

      const body: DockerCreatePayload = {
        name: name.value,
        image_id: imageId.value || null,
        image_file: imageFile.value?.id || null,
      };

      const res = await axiosInstance.post('docker_images/', body);
      if (res.status === 201) {
        ctx.emit('created', res.data);

        // Clear data
        name.value = '';
        imageId.value = '';
      }
    }

    const fileUploadDialog = ref(false);
    function fileUploaded(files: ChecksumFile[]) {
      [imageFile.value] = files;
      imageId.value = '';
      fileUploadDialog.value = false;
    }

    const fileSelectDialog = ref(false);
    const selectedFiles = ref<ChecksumFile[]>([]);
    watch(selectedFiles, (files) => {
      [imageFile.value] = files;
      imageId.value = '';
    });

    function clearImageFile() {
      selectedFiles.value = [];
      imageFile.value = undefined;
    }

    return {
      name,
      imageId,
      imageFile,
      createDisabled,
      createDockerImage,
      fileUploadDialog,
      fileUploaded,
      fileSelectDialog,
      selectedFiles,
      clearImageFile,
    };
  },
});
</script>

<template>
  <v-card>
    <v-card-title>
      Create a new Docker Image
      <v-spacer />
      <v-btn
        class="mx-1"
        color="success"
        :disabled="createDisabled"
        @click="createDockerImage"
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
        label="Name"
        :rules="[(val) => (!!val || 'This field is required')]"
      />
      <v-text-field
        v-model="imageId"
        label="Image ID"
        :disabled="!!imageFile"
      />

      <v-subheader class="pl-0">
        Image File
      </v-subheader>
      <v-row
        no-gutters
        align="center"
      >
        <v-dialog
          v-model="fileUploadDialog"
          width="60vw"
        >
          <template v-slot:activator="{ on }">
            <v-btn
              text
              class="mr-1"
              :disabled="!!imageId"
              v-on="on"
            >
              <v-icon left>
                mdi-cloud-upload
              </v-icon>
              Upload
            </v-btn>
          </template>
          <upload-dialog
            single
            @complete="fileUploaded"
          />
        </v-dialog>
        <span :class="!!imageId ? 'text--disabled': 'font-weight-bold'">OR</span>
        <v-dialog
          v-model="fileSelectDialog"
          width="60vw"
        >
          <template v-slot:activator="{ on }">
            <v-btn
              text
              class="ml-1"
              :disabled="!!imageId"
              v-on="on"
            >
              <v-icon left>
                mdi-file
              </v-icon>
              Select Existing File
            </v-btn>
          </template>
          <v-card>
            <v-card-title class="pl-3">
              Select File
            </v-card-title>
            <file-selector
              v-model="selectedFiles"
              single
            />
          </v-card>
        </v-dialog>
        <span
          v-if="imageFile"
          class="ml-1"
        >
          {{ imageFile.name }}
        </span>
        <v-spacer />
        <v-btn
          v-if="!!imageFile"
          icon
          color="error"
          @click="clearImageFile"
        >
          <v-icon>
            mdi-delete-sweep
          </v-icon>
        </v-btn>
      </v-row>
    </v-card-text>
  </v-card>
</template>
