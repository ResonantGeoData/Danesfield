export function LE90(C2_2: number) {
  return 1.6499 * Math.sqrt(C2_2);
}

export function R(r: number) {
  const vals = [
    1.6449,
    1.6456,
    1.6479,
    1.6518,
    1.6573,
    1.6646,
    1.6738,
    1.6852,
    1.6992,
    1.7163,
    1.7371,
    1.7621,
    1.7915,
    1.8251,
    1.8625,
    1.9034,
    1.9472,
    1.9936,
    2.0424,
    2.0932,
    2.1460,
  ];
  const n = vals.length - 1;
  const ndx = Math.floor(n * r);
  return vals[ndx];
}

export function eigenv2x2(C0_0: number, C0_1: number, C1_0: number, C1_1: number) {
  // char poly: x^2 - (a+d)x + (ad-bc) = 0
  const [a, b, c, d] = [C0_0, C0_1, C1_0, C1_1];
  const p = a + d;
  const q = a * d - b * c;
  const r = Math.sqrt(p * p - 4 * q);
  const vmax = 0.5 * (p + r);
  const vmin = 0.5 * (p - r);
  return [vmax, vmin];
}

export function CE90(C0_0: number, C1_0: number, C1_1: number) {
  const [vmax, vmin] = eigenv2x2(C0_0, C1_0, C1_0, C1_1);
  const smax = Math.sqrt(vmax);
  const smin = Math.sqrt(vmin);
  const r = smin / smax;
  return R(r) * smax;
}
