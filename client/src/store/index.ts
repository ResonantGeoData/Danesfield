import { ref } from '@vue/composition-api';

// eslint-disable-next-line import/prefer-default-export
export const openFile = ref('');

export function setOpenFile(newFile: string) {
  openFile.value = newFile;
}
