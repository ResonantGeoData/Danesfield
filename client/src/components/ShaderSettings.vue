<script setup lang="ts">
import {
  ref, PropType, watchEffect, computed,
} from 'vue';
import type { ComputedRef } from 'vue';
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

const shaderOptions: ComputedRef<{
  title: string;
  propertyName?: string;
  sourceMin: number;
  sourceMax: number;
}[]> = computed(() => {
  // TODO: calculate these manually once Cesium supports it. For now, just hardcode
  // the values for the datasets we care about.
  switch (props.tiles3d[props.tiles3dId].source.name) {
    case 'ucsd-all-region':
      return [
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
    case 'ucsd-full-region-self-error':
      return [
        createShaderOption('Default', undefined, 0.0, 1.0),
        createShaderOption('C 0_0', 'c0_0', 0.08187296986579895, 2.7708709239959717e-05),
        createShaderOption('C 1_0', 'c1_0', -1.1274002645222936e-05, 8.595945473643951e-06),
        createShaderOption('C 1_1', 'c1_1', 0.08102615922689438, 1.3262033462524414e-05),
        createShaderOption('C 2_0', 'c2_0', 0.005069461185485125, 0.00010266946628689766),
        createShaderOption('C 2_1', 'c2_1', -0.008007237687706947, 8.565373718738556e-06),
        createShaderOption('C 2_2', 'c2_2', 0.16099649667739868, 0.0001596212387084961),
        createShaderOption('LE90', undefined, 0.6620119598393063, 0.0003280971701203894),
        createShaderOption('CE90', undefined, 0.5989373493306599, 0.00010082366752983685),
      ];
    case 'ucsd-all-total-error':
      return [
        createShaderOption('Default', undefined, 0.0, 1.0),
        createShaderOption('C 0_0', 'c0_0', 0.12492009997367859, 0.18175694346427917),
        createShaderOption('C 1_0', 'c1_0', -0.03651577606797218, 0.19667799770832062),
        createShaderOption('C 1_1', 'c1_1', 0.1556130051612854, 0.3247891366481781),
        createShaderOption('C 2_0', 'c2_0', -0.7162777185440063, 0.8980929851531982),
        createShaderOption('C 2_1', 'c2_1', -1.0689252614974976, 0.8836731910705566),
        createShaderOption('C 2_2', 'c2_2', 1.571554183959961, 2.259568214416504),
        createShaderOption('LE90', undefined, 2.068341767857969, 1.1610492734220559),
        createShaderOption('CE90', undefined, 0.7899198029969414, 0.5694263650359508),
      ];
    default:
      return [];
  }
});

watchEffect(() => {
  const current = props.tiles3d[props.tiles3dId];
  const tilesetURL = `${axiosInstance.defaults.baseURL}/datasets/${props.datasetId}/file/${current.source.json_file.name}`;
  const { scene } = cesiumViewer.value;
  const { primitives } = scene;

  if (!colorMapOptions.value.includes(colormap.value)) {
    [colormap.value] = colorMapOptions.value;
  }

  const selectedShader = shaderOptions.value.find((s) => s.title === shader.value);

  if (!selectedShader) {
    throw Error('Shader not found!!');
  }

  // Check if this tileset is already downloaded. If it is, show/hide it and return.
  for (let i = 0; i < primitives.length; i += 1) {
    const currentTileset = primitives.get(i);
    // eslint-disable-next-line no-underscore-dangle
    if (currentTileset._url === tilesetURL) {
      currentTileset.customShader = createShader(
        props.tiles3dId,
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
  <v-menu
    v-model="menu"
    :close-on-content-click="false"
    :nudge-width="200"
    offset-y
    bottom
    left
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
            :id="`canvas-${tiles3dId}`"
            :style="`display: ${shader === 'Default' ? 'none' : 'block'};`"
            class="mx-3 justify-center"
          />
        </v-list-item>
      </v-list>
    </v-card>
  </v-menu>
</template>
