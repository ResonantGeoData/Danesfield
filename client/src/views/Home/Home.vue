<script lang="ts">
import {
  defineComponent, onMounted, ref, watch,
} from '@vue/composition-api';
import { axiosInstance } from '@/api';
import { Dataset, Task } from '@/types';

import CreateDataset from './components/CreateDataset.vue';

export default defineComponent({
  name: 'Home',
  components: {
    CreateDataset,
  },
  setup(props, ctx) {
    const router = ctx.root.$router;
    function viewTask(id: number) {
      // router.push({ name: 'danesfield', params: { id: id.toString() } });
      router.push({ name: 'danesfield' });
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

    const tasks = ref<Task[]>([]);
    const fetchingTasks = ref(false);
    const fetchTasks = async () => {
      fetchingTasks.value = true;
      try {
        // eslint-disable-next-line @typescript-eslint/camelcase
        const res = await axiosInstance.get('tasks/', { params: { algorithm__pk: 1 } });
        tasks.value = res.data.results;
      } catch (error) {
        // TOOD: Handle
      }

      fetchingTasks.value = false;
    };

    onMounted(() => {
      fetchDatasets();
      fetchTasks();
    });

    return {
      datasets,
      datasetCreated,
      datasetDialogOpen,
      showOutputDatasets,
      fetchingDatasets,

      tasks,
      fetchingTasks,
      viewTask,
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
      <v-col cols="6">
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

      <v-col cols="6">
        <v-card
          flat
          outlined
          style="height: 100%"
        >
          <v-progress-linear
            v-show="fetchingTasks"
            indeterminate
          />
          <v-card-title>Tasks</v-card-title>
          <v-list dense>
            <v-list-item
              v-for="task in tasks"
              :key="task.id"
              class="my-2"
              dense
            >
              <v-card
                width="100%"
                @click="viewTask(task.id)"
              >
                <v-card-title>{{ task.id }}</v-card-title>
                <v-card-text>
                  Status: "{{ task.status }}"<br>

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
