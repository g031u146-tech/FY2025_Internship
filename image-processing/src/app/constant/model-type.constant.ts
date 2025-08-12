/**
 * 物体検知
 */
export const DETECTION = 0x00;
/**
 * セグメンテーション
 */
export const SEGMENTATION = 0x01;
/**
 * 姿勢推定
 */
export const POSE = 0x02;
/**
 * 指向性検出
 */
export const CLASS = 0x04;
/**
 * 動体検知
 */
export const MOTION = 0xFF;

export const models: {
    [key: string] : string} = {
        [DETECTION]: '物体検出',
        [SEGMENTATION]: 'セグメンテーション',
        [POSE]: '姿勢推定',
        //[this.OBB]: '指向性検出',
        [CLASS]: '画像分類',
        //[this.MOTION]: '動体検知'
  };