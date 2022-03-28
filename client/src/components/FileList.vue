<template>
  <v-simple-table>
    <template v-slot:default>
      <thead>
        <tr>
          <th class="text-left">
            File Name
          </th>
          <th class="text-left">
            File Type
          </th>
          <th class="text-left">
            Actions
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="tileset in tiles3d"
          :key="tileset.spatial_id"
        >
          <td>{{ tileset.source.name }}</td>
          <td>3D Tiles</td>
          <td>
            <v-btn
              icon
              @click="setTiles3dVisibility(tileset.spatial_id)"
            >
              <v-icon :color="tiles3dIsVisible(tileset.spatial_id) ? 'success' : ''">
                mdi-eye
              </v-icon>
            </v-btn>
          </td>
        </tr>
        <tr
          v-for="raster in rasters"
          :key="raster.spatial_id"
        >
          <td>{{ raster.parent_raster.name }}</td>
          <td>Raster</td>
          <td>
            <v-btn
              icon
              @click="setRasterVisibility(raster.spatial_id)"
            >
              <v-icon :color="rasterIsVisible(raster.spatial_id) ? 'success' : ''">
                mdi-eye
              </v-icon>
            </v-btn>
          </td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
</template>

<script lang="ts">
import {
  defineComponent, ref, PropType, onMounted,
} from '@vue/composition-api';
import { axiosInstance } from '@/api';
import { addVisibleOverlay, visibleOverlayIds } from '@/store/cesium/layers';
import { cesiumViewer } from '@/store/cesium';
import Cesium from '@/plugins/cesium';
import { Cesium3DTileset } from 'cesium';
import { addFootprint } from '@/store/cesium/footprints';

export default defineComponent({
  name: 'FileList',
  props: {
    datasetId: {
      type: String,
      required: true,
    },
    rasterIds: {
      type: Array as PropType<number[]>,
      required: true,
    },
    meshIds: {
      type: Array as PropType<number[]>,
      required: true,
    },
    tiles3dIds: {
      type: Array as PropType<number[]>,
      required: true,
    },
  },
  setup(props) {
    const rasters = ref<any[]>([]);
    const tiles3d = ref<any[]>([]);

    function rasterIsVisible(rasterId: number) {
      return visibleOverlayIds.value?.includes(rasterId);
    }

    async function setRasterVisibility(rasterId: number) {
      if (rasterIsVisible(rasterId)) {
        visibleOverlayIds.value = visibleOverlayIds.value?.filter((id) => id !== rasterId);
      } else {
        addVisibleOverlay(rasterId);
      }
    }

    function tiles3dIsVisible(tiles3dId: number) {
      const current: any = tiles3d.value.filter((tile: any) => tile.spatial_id === tiles3dId)[0];
      const tilesetURL = `${axiosInstance.defaults.baseURL}/datasets/${props.datasetId}/file/${current.source.json_file.name}`;
      const { scene } = cesiumViewer.value;
      const { primitives } = scene;
      for (let i = 0; i < primitives.length; i += 1) {
        // eslint-disable-next-line no-underscore-dangle
        if (primitives.get(i)._url === tilesetURL) {
          return true;
        }
      }
      return false;
    }

    async function setTiles3dVisibility(tiles3dId: number) {
      const current: any = tiles3d.value.filter((tile: any) => tile.spatial_id === tiles3dId)[0];
      const tilesetURL = `${axiosInstance.defaults.baseURL}/datasets/${props.datasetId}/file/${current.source.json_file.name}`;
      const { scene } = cesiumViewer.value;
      const { primitives } = scene;

      // Check if this tileset is already displayed. If it is, remove it and return.
      for (let i = 0; i < primitives.length; i += 1) {
        const currentTileset = primitives.get(i);
        // eslint-disable-next-line no-underscore-dangle
        if (currentTileset._url === tilesetURL) {
          cesiumViewer.value.scene.primitives.remove(currentTileset);
          return;
        }
      }

      // Otherwise, display it.
      const tileset: Cesium3DTileset = new Cesium.Cesium3DTileset({
        url: tilesetURL,
      });
      cesiumViewer.value.scene.primitives.add(tileset);

      addFootprint(current.spatial_id);
    }

    onMounted(async () => {
      await Promise.all(props.rasterIds.map(async (id) => {
        const { data } = await axiosInstance.get(`/rgd_imagery/raster/${id}`);
        rasters.value.push(data);
      }));

      await Promise.all(props.tiles3dIds.map(async (id) => {
        // console.log(id);
        const { data } = await axiosInstance.get(`/rgd_3d/tiles3d/${id}`);
        tiles3d.value.push(data);
      }));

      if (tiles3d.value.length > 0) {
        setTiles3dVisibility(tiles3d.value[0].spatial_id);
      } else if (rasters.value.length > 0) {
        setRasterVisibility(rasters.value[0].spatial_id);
      }
    });

    return {
      rasters,
      tiles3d,
      rasterIsVisible,
      setRasterVisibility,
      tiles3dIsVisible,
      setTiles3dVisibility,
    };
  },
});
</script>
