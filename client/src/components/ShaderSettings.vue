<script setup lang="ts">
import { ref, watchEffect, computed } from 'vue';
import type { Ref, PropType } from 'vue';
import * as Cesium from 'cesium';
import { createShader } from '@/utils/cesium';
import { CE90, LE90 } from '@/utils/error';
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
    case 'cdist':
      return ['plasma', 'cool', 'warm', 'inferno'];
    case 'Default':
      return [];
    default:
      return ['greys'];
  }
});

const colormap = ref('');

const shaderOptions: Ref<{
  propertyName?: string;
  sourceMin: number;
  sourceRange: number;
}[]> = ref([]);

watchEffect(async () => {
  const current = props.tiles3d[props.tiles3dId];
  const tilesetURL = `${axiosInstance.defaults.baseURL}/datasets/${props.datasetId}/file/${current.source.json_file.name}`;
  const { scene } = cesiumViewer.value;
  const { primitives } = scene;
  for (let i = 0; i < primitives.length; i += 1) {
    const primitive = primitives.get(i);
    /* eslint-disable no-underscore-dangle */
    if (primitive._url === tilesetURL) {
      primitive.tileVisible.addEventListener((tile: Cesium.Cesium3DTile) => {
        if (shaderOptions.value.length > 0) {
          return;
        }

        // Add default texture to shader dropdown
        shaderOptions.value.unshift({
          propertyName: 'Default',
          sourceMin: 0.0,
          sourceRange: 1.0,
        });

        // We're using a private API here, so wrap this in a try/catch so any errors don't
        // crash the entire app.
        try {
        // @ts-ignore
          const { properties } = tile._content._model.structuralMetadata?._propertyTextures[0];

          // Add covariance values to dropdown
          shaderOptions.value.push(...Object.entries(properties).map(
            ([propertyName, propertyValues]: [string, any]) => ({
              propertyName,
              sourceMin: propertyValues._offset,
              sourceRange: propertyValues._scale,
            }),
          ));

          // Calculate LE90/CE90 values and add them to dropdown
          /* eslint-disable camelcase */
          const C0_0_min = properties.c0_0._offset;
          const C0_0_max = C0_0_min + properties.c0_0._scale;

          const C1_0_min = properties.c1_0._offset;
          const C1_0_max = C1_0_min + properties.c1_0._scale;

          const C1_1_min = properties.c1_1._offset;
          const C1_1_max = C1_1_min + properties.c1_1._scale;

          const C2_2_min = properties.c2_2._offset;
          const C2_2_max = C2_2_min + properties.c2_2._scale;

          const LE90_values = {
            propertyName: 'LE90',
            sourceMin: LE90(C2_2_min),
            sourceRange: LE90(C2_2_max) - LE90(C2_2_min),
          };
          if (LE90_values.sourceMin && LE90_values.sourceRange) {
            shaderOptions.value.push(LE90_values);
          }

          const CE90_values = {
            propertyName: 'CE90',
            sourceMin: CE90(C0_0_min, C1_0_min, C1_1_min),
            sourceRange: CE90(C0_0_max, C1_0_max, C1_1_max) - CE90(C0_0_min, C1_0_min, C1_1_min),
          };
          if (CE90_values.sourceMin && CE90_values.sourceRange) {
            shaderOptions.value.push(CE90_values);
          }
          /* eslint-enable camelcase */
        } catch (e) {
          // ignore
        }
      });
    }
    /* eslint-enable no-underscore-dangle */
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

  const selectedShader = shaderOptions.value.find((s) => s.propertyName === shader.value);

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
        selectedShader?.propertyName,
        selectedShader.sourceMin,
        selectedShader.sourceRange,
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
        :loading="!disabled && shaderOptions.length === 0"
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
            :items="shaderOptions.map((o) => o.propertyName)"
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
