import { ref } from '@vue/composition-api';

export const selectedTab = ref('regions');

export const drawerContents = ref();

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const clearMetaDataDrawer = (_spatialId?: number, _region?: boolean) => {
  drawerContents.value = undefined;
};

// eslint-disable-next-line import/prefer-default-export
export const openFile = ref('');

export function setOpenFile(newFile: string) {
  openFile.value = newFile;
}
