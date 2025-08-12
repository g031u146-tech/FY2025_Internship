import { Component, Inject } from '@angular/core';
import { Subject } from "rxjs";
import { FormsModule, } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogRef, MatDialogContent, MatDialogActions, MatDialogTitle, MatDialogClose, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import * as Services from '../../service/';

@Component({
  selector: 'app-change-setting-camera-dialog',
  standalone: true,
  imports: [
    FormsModule,
    MatButtonModule,
    MatDialogContent, MatDialogActions, MatDialogTitle, MatDialogClose,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    MatSlideToggleModule,
  ],
  templateUrl: './change-setting-camera-dialog.component.html',
  styleUrl: './change-setting-camera-dialog.component.scss'
})
export class ChangeSettingCameraDialogComponent {
  /** 名称 */
  private name: string = '';
  /** マスキングフラグ */
  private isMasking: boolean = false;

  /**
   * コンストラクタ
   * @param dialogRef 
   * @param data 
   */
  constructor(private dialogRef: MatDialogRef<ChangeSettingCameraDialogComponent>, @Inject(MAT_DIALOG_DATA) private data: any) {
    this.name = data.name;
    this.isMasking = data.isMasking;
  }

/**
 * 変更ボタンイベント
 */
onConfirm(): void {
}

/**
 * 閉じるボタンイベント
 */
  onClose(): void{
    this.dialogRef.close();
  }
}
