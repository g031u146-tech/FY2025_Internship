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
import { TransmissionType, ClientType } from '../../constant';
import { identifierName } from '@angular/compiler';

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
  protected name: string = '';
  /** マスキングフラグ */
  protected isMasking: boolean = false;

  protected errorMessage: string = ''

  /**
   * コンストラクタ
   * @param dialogRef 
   * @param data 
   */
  constructor(public dialogRef: MatDialogRef<ChangeSettingCameraDialogComponent>, @Inject(MAT_DIALOG_DATA) public data: any) {
    this.name = data.name;
    this.isMasking = data.isMasking;
  }



  /**
   * 変更ボタンイベント
   */
   /* @param {number} id カメラID
   * @param {string} name 名称
   * @param {boolean} isMasking マスキングフラグ
   */
  onConfirm(): void {
    if( confirm('変更しますか？') ) {
        this.data.websocket.Subject$.next(JSON.stringify(
              {
                'transmissionType': TransmissionType.CHANGE_CAMERA_SETTINGS,
                 'id': this.data.id,
                'name': this.name,
                'isMasking':this.isMasking,
              }
            ));
        return;
    }
  }



/**
 * 閉じるボタンイベント
 */
  onClose(): void{
    if( confirm('キャンセルしますか？') ) {
        console.log('はい');
        this.dialogRef.close()
        return
    }  
  }

  updateErrorMessage(): void{
    this.errorMessage = '';

    if (this.name.length == 0) {
      this.errorMessage = 'カメラ名称を入力してください。';
    }
  }
}
