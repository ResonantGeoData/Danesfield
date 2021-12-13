<script lang="ts">
import {
  defineComponent, onMounted, ref, watch,
} from '@vue/composition-api';
import { axiosInstance } from '@/api';
import {
  DockerImage, Algorithm, Dataset,
} from '@/types';

import CreateAlgorithm from './components/CreateAlgorithm.vue';
import CreateDataset from './components/CreateDataset.vue';
import CreateDockerImage from './components/CreateDockerImage.vue';

export default defineComponent({
  name: 'Home',
  components: {
    CreateAlgorithm,
    CreateDataset,
    CreateDockerImage,
  },
  setup(props, ctx) {
    const router = ctx.root.$router;
    function viewAlgorithm(id: number) {
      router.push({ name: 'algorithm', params: { id: id.toString() } });
    }

    const datasets = ref<Dataset[]>([]);
    const datasetDialogOpen = ref(false);
    const showOutputDatasets = ref(false);
    const fetchingDatasets = ref(false);
    const fetchDatasets = async () => {
      fetchingDatasets.value = true;

      try {
        const res = await axiosInstance.get('datasets/', {
          params: {
            // eslint-disable-next-line @typescript-eslint/camelcase
            include_output_datasets: showOutputDatasets.value,
          },
        });

        datasets.value = res.data.results;
      } catch (error) {
        // TODO: Handle
      }

      fetchingDatasets.value = false;
    };

    // Update list if output datasets are desired
    watch(showOutputDatasets, fetchDatasets);

    const datasetCreated = () => {
      datasetDialogOpen.value = false;
      fetchDatasets();
    };

    const dockerImages = ref<DockerImage[]>([]);
    const dockerImageDialogOpen = ref(false);
    const fetchingDockerImages = ref(false);
    const fetchDockerImages = async () => {
      fetchingDockerImages.value = true;

      try {
        const res = await axiosInstance.get('docker_images/');
        dockerImages.value = res.data.results;
      } catch (error) {
        // TODO: Handle
      }

      fetchingDockerImages.value = false;
    };

    const dockerImageCreated = () => {
      dockerImageDialogOpen.value = false;
      fetchDockerImages();
    };

    const algorithms = ref<Algorithm[]>([]);
    const fetchingAlgorithms = ref(false);
    const algorithmDialogOpen = ref(false);
    const fetchAlgortihms = async () => {
      fetchingAlgorithms.value = true;
      try {
        const res = await axiosInstance.get('algorithms/');
        algorithms.value = res.data.results;
      } catch (error) {
        // TOOD: Handle
      }

      fetchingAlgorithms.value = false;
    };

    onMounted(() => {
      fetchDatasets();
      fetchDockerImages();
      fetchAlgortihms();
    });

    return {
      datasets,
      datasetCreated,
      datasetDialogOpen,
      showOutputDatasets,
      fetchingDatasets,

      dockerImages,
      dockerImageDialogOpen,
      dockerImageCreated,
      fetchingDockerImages,

      algorithms,
      fetchingAlgorithms,
      algorithmDialogOpen,
      viewAlgorithm,
    };
  },
});
</script>

<template>
  <v-container
    fill-height
    style="align-items: start"
  >
    <v-row style="height: 100%; max-height: 100%">
      <v-col cols="4">
        <v-card
          flat
          outlined
          style="height: 100%"
        >
          <v-progress-linear
            v-show="fetchingDockerImages"
            indeterminate
          />
          <v-card-title>
            Docker Images
            <v-dialog
              v-model="dockerImageDialogOpen"
              width="50vw"
            >
              <template v-slot:activator="{ on }">
                <v-btn
                  icon
                  right
                  small
                  v-on="on"
                >
                  <v-icon color="success">
                    mdi-plus-circle
                  </v-icon>
                </v-btn>
              </template>
              <create-docker-image @created="dockerImageCreated" />
            </v-dialog>
          </v-card-title>
          <v-list>
            <v-list-item
              v-for="image in dockerImages"
              :key="image.id"
              class="my-2"
            >
              <v-card width="100%">
                <v-card-title>{{ image.name }}</v-card-title>
                <v-card-text>
                  Image ID: {{ image.image_id }}<br>
                  Image file: {{ image.image_file || 'null' }}<br>
                  <!-- Uses GPU: {{ alg.gpu }}<br> -->
                </v-card-text>
              </v-card>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>

      <v-col cols="4">
        <v-card
          flat
          outlined
          style="height: 100%"
        >
          <v-progress-linear
            v-show="fetchingDatasets"
            indeterminate
          />
          <v-card-title>
            Datasets
            <v-dialog
              v-model="datasetDialogOpen"
              width="50vw"
            >
              <template v-slot:activator="{ on }">
                <v-btn
                  icon
                  right
                  small
                  v-on="on"
                >
                  <v-icon color="success">
                    mdi-plus-circle
                  </v-icon>
                </v-btn>
              </template>
              <create-dataset @created="datasetCreated" />
            </v-dialog>
            <v-spacer />
            <v-switch
              v-model="showOutputDatasets"
              label="Show output datasets"
              hide-details
              class="mt-0"
            />
          </v-card-title>
          <v-list dense>
            <v-list-item
              v-for="ds in datasets"
              :key="ds.id"
              class="my-2"
              dense
            >
              <v-card
                width="100%"
              >
                <v-card-title>{{ ds.name }}</v-card-title>
                <v-card-text>
                  Number of files: {{ ds.files.length }}
                </v-card-text>
              </v-card>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>

      <v-col cols="4">
        <v-card
          flat
          outlined
          style="height: 100%"
        >
          <v-progress-linear
            v-show="fetchingAlgorithms"
            indeterminate
          />
          <v-card-title>
            Algorithms
            <v-dialog
              v-model="algorithmDialogOpen"
              width="50vw"
            >
              <template v-slot:activator="{ on }">
                <v-btn
                  icon
                  right
                  small
                  v-on="on"
                >
                  <v-icon color="success">
                    mdi-plus-circle
                  </v-icon>
                </v-btn>
              </template>
              <create-algorithm />
            </v-dialog>
          </v-card-title>
          <v-list dense>
            <v-list-item
              v-for="alg in algorithms"
              :key="alg.id"
              class="my-2"
              dense
            >
              <v-card
                width="100%"
                @click="viewAlgorithm(alg.id)"
              >
                <v-card-title>{{ alg.name }}</v-card-title>
                <v-card-text>
                  Command: "{{ alg.command }}"<br>
                  Uses GPU: {{ alg.gpu }}<br>

                  <!-- TODO: Num files -->
                  <!-- TODO: Num tasks -->
                  <!-- TODO: Currently running tasks (bool) -->
                </v-card-text>
              </v-card>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
