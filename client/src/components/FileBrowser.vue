<template>
  <v-card
    height="100%"
    outlined
  >
    <v-btn
      icon
      :to="{ name: 'explore' }"
    >
      <v-icon>
        mdi-arrow-left
      </v-icon>
    </v-btn>
    <v-card-title>
      <template v-for="part in splitLocation">
        /{{ part }}
      </template>
    </v-card-title>
    <v-progress-linear
      v-if="updating"
      indeterminate
    />
    <v-divider v-else />
    <v-list>
      <v-list-item
        v-for="item in items"
        :key="item.path"
        color="primary"
        @click="selectPath(item)"
      >
        <v-icon
          class="mr-2"
          color="primary"
        >
          <template v-if="item.isFolder">
            mdi-folder
          </template>
          <template v-else>
            mdi-file
          </template>
        </v-icon>
        <span class="text-truncate">
          {{ item.path }}
        </span>
        <v-spacer />

        <v-list-item-action v-if="!item.isFolder">
          <v-btn
            icon
            :href="item.file"
          >
            <v-icon color="primary">
              mdi-download
            </v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script lang="ts">
import {
  computed, defineComponent, Ref, ref, watch,
} from '@vue/composition-api';
import { axiosInstance } from '@/api';
import { RawLocation } from 'vue-router';
import { ChecksumFile } from '@/types';

const parentDirectory = '..';
const rootDirectory = '';

interface FileItem extends ChecksumFile {
  isFolder: boolean;
  path: string;
}

export default defineComponent({
  name: 'FileBrowser',
  setup(props, ctx) {
    const location = ref(rootDirectory);
    const items: Ref<FileItem[]> = ref([]);
    const updating = ref(false);

    const splitLocation = computed(() => location.value.split('/'));

    watch(location, async () => {
      updating.value = true;

      // eslint-disable-next-line @typescript-eslint/camelcase
      const { data } = await axiosInstance.get('/rgd/checksum_file/tree', { params: { path_prefix: location.value } });

      items.value = [
        ...location.value !== rootDirectory ? [{ path: parentDirectory, isFolder: true }] : [],
        ...[
          ...Object.keys(data.files).map((name: string) => (
            { isFolder: false, path: name, ...data.files[name] }
          )),
          ...Object.keys(data.folders).map((name: string) => (
            { isFolder: true, path: `${name}/`, ...data.files[name] }
          )),
        ],
      ];
      updating.value = false;
    }, { immediate: true });

    watch(location, () => {
      const { location: existingLocation } = ctx.root.$route.query;

      const route = {
        ...ctx.root.$route,
        query: { location: location.value },
      } as RawLocation;

      // Update route when location changes
      if (existingLocation === location.value) { return; }
      ctx.root.$router.push(route);
    });

    function locationSlice(index: number) {
      return `${splitLocation.value.slice(0, index + 1).join('/')}/`;
    }

    function selectPath(item: FileItem) {
      const { path, isFolder } = item;

      if (!isFolder) { return; }
      if (path === parentDirectory) {
        const slicedLocation = location.value.split('/').slice(0, -2);
        location.value = slicedLocation.length ? `${slicedLocation.join('/')}/` : '';
      } else {
        location.value = `${location.value}${path}`;
      }
    }

    return {
      items,
      splitLocation,
      updating,
      rootDirectory,
      locationSlice,
      selectPath,
    };
  },
});
</script>
