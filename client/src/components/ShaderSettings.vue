<script setup lang="ts">
import {
  ref, PropType, watchEffect, computed,
} from 'vue';
import { createShader } from '@/utils/cesium';
import { axiosInstance } from '@/api';
import type { Tiles3DMeta } from '@/types';
import { cesiumViewer } from '@/store/cesium';

const props = defineProps({
  disabled: {
    type: Boolean,
    required: true,
  },
  datasetId: {
    type: String,
    required: true,
  },
  tiles3d: {
    type: Object as PropType<Record<number, Tiles3DMeta>>,
    required: true,
  },
  tiles3dId: {
    type: Number,
    required: true,
  },
});

const menu = ref(false);
const shader = ref('Default');

const colorMapOptions = computed(() => {
  switch (shader.value) {
    case 'LE90':
    case 'CE90':
      return ['plasma', 'cool', 'warm', 'inferno'];
    case 'Default':
      return [];
    default:
      return ['greys'];
  }
});

const colormap = ref('');

function createShaderOption(
  title: string,
  propertyName: string | undefined,
  sourceMin: number,
  sourceMax: number,
) {
  return {
    title, propertyName, sourceMin, sourceMax,
  };
}

const shaderOptions: {
  title: string;
  propertyName?: string;
  sourceMin: number;
  sourceMax: number;
}[] = [
  createShaderOption('Default', undefined, 0.0, 1.0),
  createShaderOption('C 0_0', 'c0_0', 0.043, 0.181),
  createShaderOption('C 1_0', 'c1_0', -0.036, 0.196),
  createShaderOption('C 1_1', 'c1_1', 0.074, 0.324),
  createShaderOption('C 2_0', 'c2_0', -0.072, 0.897),
  createShaderOption('C 2_1', 'c2_1', -1.06, 0.883),
  createShaderOption('C 2_2', 'c2_2', 1.41, 2.259),
  createShaderOption('LE90', undefined, 1.959, 1.201),
  createShaderOption('CE90', undefined, 0.531, 0.689),
];

watchEffect(() => {
  const current = props.tiles3d[props.tiles3dId];
  const tilesetURL = `${axiosInstance.defaults.baseURL}/datasets/${props.datasetId}/file/${current.source.json_file.name}`;
  const { scene } = cesiumViewer.value;
  const { primitives } = scene;

  if (!colorMapOptions.value.includes(colormap.value)) {
    [colormap.value] = colorMapOptions.value;
  }

  const selectedShader = shaderOptions.find((s) => s.title === shader.value);

  if (!selectedShader) {
    throw Error('Shader not found!!');
  }

  // Check if this tileset is already downloaded. If it is, show/hide it and return.
  for (let i = 0; i < primitives.length; i += 1) {
    const currentTileset = primitives.get(i);
    // eslint-disable-next-line no-underscore-dangle
    if (currentTileset._url === tilesetURL) {
      currentTileset.customShader = createShader(
        shader.value,
        selectedShader?.propertyName,
        selectedShader.sourceMin,
        selectedShader.sourceMax,
        colormap.value,
      );
    }
  }
});

</script>

<template>
  <!-- <div class="text-center"> -->
  <v-menu
    v-model="menu"
    :close-on-content-click="false"
    :nudge-width="200"
    offset-x
  >
    <template #activator="{ on, attrs }">
      <v-btn
        :disabled="disabled"
        icon
        v-bind="attrs"
        v-on="on"
      >
        <v-icon>mdi-texture</v-icon>
      </v-btn>
    </template>

    <v-card>
      <v-list>
        <v-list-item>
          <v-select
            v-model="shader"
            class="mx-2"
            style="width: 8em; display: inline-flex;"
            :items="shaderOptions.map((o) => o.title)"
            label="Shader"
            outlined
          />
          <v-select
            v-model="colormap"
            class="mx-2"
            style="width: 8em; display: inline-flex;"
            :items="colorMapOptions"
            label="Colormap"
            outlined
          />
        </v-list-item>

        <v-list-item>
          <canvas
            id="canvas"
            :style="`${shader === 'Default' ? 'display: none' : ''}`"
            class="mx-3 justify-end"
          />
        </v-list-item>
      </v-list>
    </v-card>
  </v-menu>
  <!-- </div> -->
</template>
