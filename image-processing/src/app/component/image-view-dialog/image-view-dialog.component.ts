import { CommonModule } from '@angular/common';
import { Component, Inject  } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogTitle, MatDialogContent, MatDialogActions, MatDialogClose } from '@angular/material/dialog';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import * as Services from '../../service/';

@Component({
  selector: 'app-image-view-dialog',
  standalone: true,
  imports: [
    CommonModule,
    MatButtonModule,
    MatDialogTitle, MatDialogContent, MatDialogActions, MatDialogClose,
    MatSlideToggleModule,
  ],
  templateUrl: './image-view-dialog.component.html',
  styleUrl: './image-view-dialog.component.scss'
})

/**
 * 画像表示ダイアログコンポーネント
 */
export class ImageViewDialogComponent {
  /** マスキングフラグ */
  protected isMasking: boolean = false;

  /**
   * コンストラクタ
   * @param dialogRef ダイアログ参照
   * @param data ダイアログデータ
   */
  constructor (private dialogRef: MatDialogRef<ImageViewDialogComponent>, @Inject(MAT_DIALOG_DATA) public data: any) {
    /** マスキングフラグ */
    this.isMasking = data.isMasking;
  }
  
  /**
   * マスキングスライドトグル切り替え処理
   */
  changeMaskingSliedToggle(): void {
  }
  
  /**
   * 閉じるボタンイベント
   */
  onClose(): void{
    this.dialogRef.close();
  }
}
