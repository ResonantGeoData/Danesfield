/// <reference types="jest" />

import {
  LE90, CE90, eigenv2x2, R,
} from '@/utils/error';

describe('LE90/CE90 functions', () => {
  test.each([
    [
      0.08187296986579895,
      -0.000011274002645222936,
      -0.000011274002645222936,
      0.08102615922689438,
      [0.08187311993549407, 0.08102600915719926],
    ],
  ])('Eigenvalues calculation', (C0_0: number, C0_1: number, C1_0: number, C1_1: number, eigenvalues: number[]) => {
    expect(eigenv2x2(C0_0, C0_1, C1_0, C1_1)).toEqual(eigenvalues);
  });

  test.each([
    [0.9948132343455307, 2.0932],
  ])('R function', (r: number, expected: number) => {
    expect(R(r)).toBeCloseTo(expected);
  });

  test.each([
    [1.41, 1.9591477009403857],
    [0.16099649667739868, 0.6620119598393063],
    [1.571554183959961, 2.068341767857969],
  ])('LE90', (C2_2: number, expected: number) => {
    expect(LE90(C2_2)).toBe(expected);
  });

  test.each([
    [0.08187296986579895, -1.1274002645222936e-05, 0.08102615922689438, 0.5989373493306599],
    [0.12492009997367859, -0.03651577606797218, 0.1556130051612854, 0.7899198029969414],
  ])('CE90', (C0_0: number, C1_0: number, C1_1: number, expected: number) => {
    expect(CE90(C0_0, C1_0, C1_1)).toBe(expected);
  });
});
