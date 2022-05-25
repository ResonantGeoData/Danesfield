<script lang="ts">
import {
  defineComponent, ref, onMounted, computed, watch, watchEffect,
} from 'vue';
import filesize from 'filesize';

import { axiosInstance } from '@/api';
import {
  Algorithm, ChecksumFile, Dataset, Task,
} from '@/types';
import UploadDialog from '@/components/UploadDialog.vue';
import CreateDataset from '@/components/CreateDataset.vue';

const fileTableHeaders = [
  {
    text: 'Name',
    align: 'start',
    value: 'name',
  },
  {
    text: 'Type (File/Url)',
    value: 'type',
  },
  {
    text: 'Download Url',
    value: 'download_url',
  },
];

const datasetTableHeaders = [
  {
    text: 'Name',
    value: 'name',
  },
  {
    text: 'Num Files',
    value: 'files',
  },
  {
    text: 'Size',
    value: 'size',
  },
];

function taskRunning(task: Task) {
  return !['failed', 'success'].includes(task.status);
}

export default defineComponent({
  name: 'AlgorithmView',
  components: { CreateDataset },
  setup() {
    // /////////////////
    // Algorithm
    // /////////////////
    const algorithm = ref<Algorithm>();
    const showAlgorithmDetails = ref(false);
    const fetchingAlgorithm = ref(false);
    const runAlgorithmDialog = ref(false);

    // Datasets for running algorithm
    const datasetList = ref<Dataset[]>([]);
    const fetchingDatasetList = ref(false);
    const datasetToRunOn = ref<Dataset | null>(null);
    async function fetchDatasetList() {
      fetchingDatasetList.value = true;

      try {
        const res = await axiosInstance.get('datasets/');
        datasetList.value = res.data.results;
      } catch (error) {
        // TODO: Handle
      }

      fetchingDatasetList.value = false;
    }

    async function fetchAlgorithm() {
      fetchingAlgorithm.value = true;

      try {
        const res = await axiosInstance.get('danesfield/algorithm/');
        algorithm.value = res.data;
      } catch (error) {
        // TODO: Handle
      }

      fetchingAlgorithm.value = false;
    }

    // /////////////////
    // Tasks
    // /////////////////
    const tasks = ref<Task[]>([]);
    const selectedTaskIndex = ref<number | null>(null);
    const selectedTask = computed(() => (
      selectedTaskIndex.value !== null ? tasks.value[selectedTaskIndex.value] : null
    ));

    function fetchTasks() {
      // eslint-disable-next-line @typescript-eslint/camelcase
      axiosInstance.get('tasks/', { params: { algorithm__pk: 1 } }).then((res) => {
        tasks.value = res.data.results.sort(
          (a: Algorithm, b: Algorithm) => -a.created.localeCompare(b.created),
        );

        // Set default to most recent, if there are any
        if (tasks.value.length && selectedTaskIndex.value === null) {
          selectedTaskIndex.value = 0;
        }
      });
    }

    // Fetch tasks until all are completed
    watchEffect(async () => {
      if (tasks.value.some((task) => taskRunning(task))) {
        // Wait 5 seconds
        await new Promise((r) => setTimeout(r, 5000));

        // Fetch tasks again
        fetchTasks();
      }
    });

    function taskStatusIconStyle(task: Task): {icon: string; color: string; class?: string} {
      switch (task.status) {
        case 'created':
        case 'queued':
          return { icon: 'mdi-pause', color: '' };
        case 'running':
          return { icon: 'mdi-autorenew', color: 'primary', class: 'rotate' };
        case 'success':
          return { icon: 'mdi-check', color: 'success' };
        case 'failed':
          return { icon: 'mdi-close', color: 'error' };
        default:
          return { icon: 'mdi-help', color: 'warning' };
      }
    }

    // /////////////////
    // Selected Task
    // /////////////////
    const selectedTaskLogs = ref('');
    async function fetchSelectedTaskLogs() {
      if (selectedTask.value === null) {
        return;
      }

      const res = await axiosInstance.get(`tasks/${selectedTask.value.id}/logs/`);
      selectedTaskLogs.value = res.data;
    }

    const selectedTaskFiles = ref<{}[]>([]);
    async function fetchSelectedTaskOutput() {
      if (selectedTask.value === null) {
        return;
      }

      const res = await axiosInstance.get(`tasks/${selectedTask.value.id}/output/`);
      selectedTaskFiles.value = res.data.results;
    }

    const outputDatasetDownloadLink = computed(() => (
      selectedTask.value
        ? `${axiosInstance.defaults.baseURL}tasks/${selectedTask.value.id}/output/download`
        : null
    ));
    const selectedTaskInput = ref<ChecksumFile[]>([]);
    const fetchingSelectedTaskInput = ref(false);
    async function fetchSelectedTaskInput() {
      if (selectedTask.value === null) {
        return;
      }

      fetchingSelectedTaskInput.value = true;
      try {
        const res = await axiosInstance.get(`tasks/${selectedTask.value.id}/input/`);
        selectedTaskInput.value = res.data.results;
      } catch (error) {
        // TODO: Handle
      }

      fetchingSelectedTaskInput.value = false;
    }

    // Update input/output/logs on task switch
    watch(selectedTaskIndex, () => {
      fetchSelectedTaskLogs();
      fetchSelectedTaskInput();
      fetchSelectedTaskOutput();
    });

    // If selected task is running, fetch output and logs
    const initialTaskFetch = ref(false);
    watch(tasks, () => {
      // Ignore the first change, it's handled elsewhere
      if (!initialTaskFetch.value) {
        initialTaskFetch.value = true;
        return;
      }

      // Fetch selected task logs/output if running
      if (selectedTask.value && taskRunning(selectedTask.value)) {
        Promise.all([
          fetchSelectedTaskLogs(),
          fetchSelectedTaskOutput(),
        ]);
      }
    });

    // /////////////////
    // Misc
    // /////////////////
    async function runAlgorithm() {
      if (datasetToRunOn.value === null) {
        throw new Error('Attempted to run algorithm without an input dataset!');
      }

      const res = await axiosInstance.post('danesfield/run/', {
        // eslint-disable-next-line @typescript-eslint/camelcase
        input_dataset: datasetToRunOn.value.id,
      });

      if (res.status === 200) {
        fetchTasks();
      }

      runAlgorithmDialog.value = false;
    }

    onMounted(() => {
      fetchAlgorithm();
      fetchTasks();
      fetchDatasetList();
    });

    return {
      filesize,

      datasetTableHeaders,
      fetchDatasetList,
      fetchingDatasetList,
      datasetList,
      datasetToRunOn,

      algorithm,
      runAlgorithmDialog,
      showAlgorithmDetails,
      fetchingAlgorithm,
      fetchAlgorithm,

      tasks,
      selectedTask,
      selectedTaskIndex,
      taskStatusIconStyle,

      fileTableHeaders,
      selectedTaskInput,
      fetchingSelectedTaskInput,
      fetchSelectedTaskInput,
      selectedTaskLogs,
      selectedTaskFiles,
      outputDatasetDownloadLink,

      runAlgorithm,
    };
  },
});
</script>

<template>
  <v-container
    fluid
    fill-height
    style="align-items: start"
  >
    <v-row no-gutters>
      <v-col>
        <v-dialog>
          <template #activator="{ on }">
            <v-btn v-on="on">
              New Dataset

              <v-icon right>
                mdi-plus
              </v-icon>
            </v-btn>
          </template>
          <create-dataset />
        </v-dialog>
      </v-col>
    </v-row>
    <v-row fill-height>
      <v-col
        cols="auto"
        class="pa-0"
      >
        <v-navigation-drawer width="300">
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="text-h6">
                <v-row
                  no-gutters
                  align="center"
                >
                  Tasks
                  <v-spacer />
                  <v-dialog
                    v-model="runAlgorithmDialog"
                    width="50vw"
                  >
                    <template #activator="{ on }">
                      <v-btn
                        class="my-1"
                        v-on="on"
                      >
                        New Task
                        <v-icon right>
                          mdi-rocket-launch
                        </v-icon>
                      </v-btn>
                    </template>
                    <v-card>
                      <v-card-title>Select a dataset to run on</v-card-title>
                      <v-data-table
                        show-select
                        single-select
                        selectable-key="id"
                        :items="datasetList"
                        :headers="datasetTableHeaders"
                        :loading="fetchingDatasetList"
                        :value="datasetToRunOn ? [datasetToRunOn] : []"
                        @input="datasetToRunOn = $event[0] || null"
                      >
                        <!-- eslint-disable-next-line vue/valid-v-slot -->
                        <template #item.files="{ item }">
                          {{ item.files.length }}
                        </template>

                        <!-- eslint-disable-next-line vue/valid-v-slot -->
                        <template #item.size="{ item }">
                          {{ filesize(item.size) }}
                        </template>
                      </v-data-table>
                      <v-card-actions>
                        <v-spacer />
                        <v-btn
                          color="secondary"
                          @click="runAlgorithmDialog = false; datasetToRunOn = null;"
                        >
                          Cancel
                        </v-btn>
                        <v-btn
                          color="success"
                          :disabled="datasetToRunOn === null"
                          @click="runAlgorithm"
                        >
                          Run
                        </v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                </v-row>
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-divider />
          <v-list-item v-if="!tasks.length">
            <v-list-item-content>
              <v-list-item-subtitle>
                This algorithm has no tasks...
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list v-else>
            <!-- FIXME: For some reason, displays wrong selected after update -->
            <v-list-item-group
              v-model="selectedTaskIndex"
              color="primary"
              mandatory
            >
              <v-list-item
                v-for="task in tasks"
                :key="task.id"
              >
                {{ task.created }}
                <v-icon
                  :color="taskStatusIconStyle(task).color"
                  :class="taskStatusIconStyle(task).class || ''"
                  right
                >
                  {{ taskStatusIconStyle(task).icon }}
                </v-icon>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-navigation-drawer>
      </v-col>

      <v-col class="pa-0">
        <v-row no-gutters>
          <v-col cols="6">
            <v-sheet>
              <v-card-title>
                Input Dataset
              </v-card-title>
              <v-data-table
                :headers="fileTableHeaders"
                :items="selectedTaskInput"
                :loading="fetchingSelectedTaskInput"
              >
                <!-- eslint-disable-next-line vue/valid-v-slot -->
                <template #item.type="{ item }">
                  {{ item.type === 1 ? 'File' : 'Url' }}
                </template>
                <!-- eslint-disable-next-line vue/valid-v-slot -->
                <template #item.download_url="{ item }">
                  <a
                    :href="item.download_url"
                    target="_blank"
                  >
                    <span>Download</span>
                  </a>
                  <v-icon
                    small
                    class="mb-1"
                  >
                    mdi-open-in-new
                  </v-icon>
                </template>
              </v-data-table>
            </v-sheet>
          </v-col>
          <v-col cols="6">
            <v-sheet
              height="100%"
              class="pa-2"
            >
              <v-card-title>Task Output Log</v-card-title>
              <v-card-text>
                <v-textarea
                  outlined
                  readonly
                  :value="selectedTaskLogs"
                  fill-height
                  placeholder="This task has no output log..."
                  hide-details
                />
              </v-card-text>
            </v-sheet>
          </v-col>
        </v-row>
        <v-row
          v-if="tasks.length"
          no-gutters
        >
          <v-col>
            <v-sheet
              height="100%"
              class="pa-2"
            >
              <v-card-title>
                Task Output Files
                <v-btn
                  icon
                  right
                  color="primary"
                  :href="outputDatasetDownloadLink"
                  target="_blank"
                >
                  <v-icon>mdi-download</v-icon>
                </v-btn>
              </v-card-title>
              <v-card-text style="height: 100%">
                <v-data-table
                  :headers="fileTableHeaders"
                  :items="selectedTaskFiles"
                  item-key="id"
                  height="100%"
                >
                  <!-- eslint-disable-next-line vue/valid-v-slot -->
                  <template #item.type="{ item }">
                    {{ item.type === 1 ? 'File' : 'Url' }}
                  </template>
                  <!-- eslint-disable-next-line vue/valid-v-slot -->
                  <template #item.download_url="{ item }">
                    <a
                      :href="item.download_url"
                      target="_blank"
                    >
                      <span>Download</span>
                    </a>
                    <v-icon
                      small
                      class="mb-1"
                    >
                      mdi-open-in-new
                    </v-icon>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-sheet>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<style lang="scss">
.rotate {
  animation: rotation 1.5s infinite linear;
}
@keyframes rotation {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(359deg);
  }
}
</style>
