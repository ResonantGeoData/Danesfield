import { AxiosResponse } from 'axios';
import S3FileFieldClient from 'django-s3-file-field';

import { axiosInstance } from '@/api';
import { ChecksumFile } from '@/types';
import { computed } from '@vue/composition-api';

export const s3ffClient = computed(() => new S3FileFieldClient({
  baseUrl: process.env.VUE_APP_S3FF_BASE_URL,
  apiConfig: axiosInstance.defaults,
}));

export async function uploadFile(file: File) {
  const fieldValue = await s3ffClient.value.uploadFile(
    file,
    'rgd.ChecksumFile.file',
  );

  const res: AxiosResponse<ChecksumFile> = await axiosInstance.post('rgd/checksum_file', {
    file: fieldValue.value,
  });

  return res.data;
}

export async function uploadFiles(files: File[]) {
  // TODO: Immediately return array of refs, that track progress of each upload
  let i = 0;
  const results: ChecksumFile[] = [];
  const WORKER_POOL_SIZE = 5;
  const workerPool = Array(WORKER_POOL_SIZE).fill(undefined);
  await Promise.all(workerPool.map(async () => {
    while (i < files.length) {
      // must increment i before `await`, but after subscript operator
      // eslint-disable-next-line no-plusplus
      const file = files[i++];

      // eslint-disable-next-line no-await-in-loop
      results.push(await uploadFile(file));
    }
  }));

  return results;
}
