<script lang="ts">
import {
  computed, defineComponent, onMounted, ref,
} from '@vue/composition-api';
import VJsoneditor from 'v-jsoneditor';

import { axiosInstance } from '@/api';
import { Dataset, DockerImage } from '@/types';
import UploadDialog from '@/components/UploadDialog.vue';

const dockerImageHeaders = [
  { text: 'Name', value: 'name' },
  { text: 'Image ID', value: 'image_id' },
  { text: 'Image File', value: 'image_file' },
];

export default defineComponent({
  name: 'CreateAlgorithm',
  components: {
    VJsoneditor,
    UploadDialog,
  },
  setup(props, ctx) {
    const router = ctx.root.$router;

    // Form data
    const name = ref('');
    const command = ref('');
    const entrypoint = ref<string | null>(null);
    const gpu = ref(true);
    const dockerImage = ref<DockerImage | null>(null);
    const environment = ref({});

    // Form validation
    const nonEmptyRule = (val: unknown) => (!!val || 'This field is required');
    const formValid = ref(false);
    const customFormFieldsValid = computed(() => dockerImage.value !== null);
    const allFieldsValid = computed(() => formValid.value && customFormFieldsValid.value);

    // Docker images
    const dockerImageList = ref<DockerImage[]>([]);
    async function fetchDockerImageList() {
      // TODO: Deal with server pagination
      const dockerImageRes = await axiosInstance.get('docker_images/');
      dockerImageList.value = dockerImageRes.data.results;
    }

    // Dataset
    const datasetListLoading = ref(false);
    const datasetHeaders = [
      { text: 'Name', value: 'name' },
      { text: 'Num Files', value: 'files' },
      { text: 'Size (Bytes)', value: 'size' },
    ];
    const datasetList = ref<Dataset[]>([]);
    async function fetchdatasetList() {
      datasetListLoading.value = true;

      try {
        // TODO: Deal with server pagination
        const datasetsRes = await axiosInstance.get('datasets/');
        datasetList.value = datasetsRes.data.results;
      } catch (error) {
        // TODO: Handle
      }

      datasetListLoading.value = false;
    }

    // Intialize on mount
    onMounted(async () => {
      fetchDockerImageList();
      fetchdatasetList();
    });

    function resetForm() {
      name.value = '';
      command.value = '';
      entrypoint.value = null;
      gpu.value = true;
      dockerImage.value = null;
      environment.value = {};
    }

    async function createAlgorithm() {
      if (!allFieldsValid.value) {
        throw new Error('Attempted to create algorithm with invalid fields!');
      }

      const body = {
        name: name.value,
        command: command.value,
        entrypoint: entrypoint.value,
        gpu: gpu.value,
        // eslint-disable-next-line @typescript-eslint/camelcase
        docker_image: dockerImage.value?.id,
        environment: environment.value,
      };

      const res = await axiosInstance.post('algorithms/', body);
      if (res.status === 201) {
        router.push({ name: 'algorithm', params: { id: res.data.id.toString() } });
      }
    }

    return {
      name,
      command,
      entrypoint,
      gpu,
      dockerImage,
      environment,
      dockerImageHeaders,
      dockerImageList,
      datasetHeaders,
      datasetList,
      datasetListLoading,
      createAlgorithm,

      // Form
      nonEmptyRule,
      formValid,
      allFieldsValid,
      resetForm,
    };
  },
});
</script>

<template>
  <v-card>
    <v-card-title>
      Create a new algorithm
      <v-spacer />
      <v-btn
        class="mx-1"
        @click="resetForm"
      >
        Reset
        <v-icon right>
          mdi-jellyfish
        </v-icon>
      </v-btn>
      <v-btn
        class="mx-1"
        color="success"
        :disabled="!allFieldsValid"
        @click="createAlgorithm"
      >
        Create
        <v-icon right>
          mdi-plus
        </v-icon>
      </v-btn>
    </v-card-title>
    <v-card-text>
      <v-form v-model="formValid">
        <v-card-subtitle class="pl-0 pb-0">
          Required Fields
        </v-card-subtitle>
        <v-text-field
          v-model="name"
          label="name"
          :rules="[nonEmptyRule]"
        />
        <v-textarea
          v-model="command"
          label="Command"
          :rules="[nonEmptyRule]"
        />
        <v-dialog width="60vw">
          <template v-slot:activator="{ on }">
            <v-btn
              color="primary"
              class="mx-1"
              :outlined="!dockerImage"
              v-on="on"
            >
              Select Docker Image
              <v-icon right>
                mdi-docker
              </v-icon>
            </v-btn>
          </template>
          <v-card>
            <v-card-title>Docker Image (select one)</v-card-title>
            <v-data-table
              title="Docker Images"
              :items="dockerImageList"
              :headers="dockerImageHeaders"
              single-select
              selectable-key="id"
              show-select
              :value="dockerImage ? [dockerImage] : []"
              @input="dockerImage = $event[0] || null"
            />
          </v-card>
        </v-dialog>
        <v-card-subtitle class="pl-0 pb-0">
          Optional Fields
        </v-card-subtitle>
        <v-checkbox
          v-model="gpu"
          label="Use GPU"
        />
        <v-textarea
          v-model="entrypoint"
          label="Entrypoint"
        />
        <v-subheader
          class="pl-0"
          style="height: 30px"
        >
          Environment
        </v-subheader>
        <v-jsoneditor
          v-model="environment"
          :options="{mode: 'code', mainMenuBar: false}"
        />
      </v-form>
    </v-card-text>
  </v-card>
</template>
