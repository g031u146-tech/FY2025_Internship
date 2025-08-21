import { Component, Inject } from '@angular/core';
import { Subject, merge } from "rxjs";
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormsModule, FormControl, Validators, ReactiveFormsModule} from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogRef, MatDialogContent, MatDialogActions, MatDialogTitle, MatDialogClose, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import * as Services from '../../service/';
import { TransmissionType, ClientType } from '../../constant';
import { TestBed } from '@angular/core/testing';

@Component({
  selector: 'app-change-setting-camera-dialog',
  standalone: true,
  imports: [
    FormsModule, ReactiveFormsModule,
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
  protected initIsMasking: boolean = false;

  protected errorMessage: string = ''
  public nameTextbox = new FormControl('', [Validators.required, Validators.maxLength(20)])
  public isDisabledButton: boolean = true
  
  /**
   * コンストラクタ
   * @param dialogRef 
   * @param data 
   */
  constructor(public dialogRef: MatDialogRef<ChangeSettingCameraDialogComponent>, @Inject(MAT_DIALOG_DATA) public data: any) {
    this.name = data.name;
    this.isMasking = data.isMasking;
    this.initIsMasking = data.isMasking;
    this.nameTextbox.setValue(this.name)
    this.isDisabledButton = true
    
     merge(this.nameTextbox.statusChanges, this.nameTextbox.valueChanges)
      .pipe(takeUntilDestroyed())
      .subscribe(() => this.updateErrorMessage());
  }



  /**
   * 変更ボタンイベント
   */
   /* @param {number} id カメラID
   * @param {string} name 名称
   * @param {boolean} isMasking マスキングフラグ
   */
  onConfirm(): void {
    if(!confirm('変更しますか？') ) return
        
    this.data.websocket.Subject$.next(JSON.stringify(
    {
      'transmissionType': TransmissionType.CHANGE_CAMERA_SETTINGS,
      'id': this.data.id,
      'name': this.nameTextbox.value,
      'isMasking':this.isMasking,
    }));
  }



/**
 * 閉じるボタンイベント
 */

  onClose(): void{
    if(
      this.name == this.nameTextbox.value && this.isMasking == this.initIsMasking)
      this.dialogRef.close()
    
      else
  

    if( confirm('キャンセルしますか？') ) {
        console.log('はい');
        this.dialogRef.close()
        return
    }  
  }

  updateErrorMessage(): void{
   
   this.errorMessage = '';
    if (this.name == this.nameTextbox.value && this.isMasking == this.initIsMasking)
      this.isDisabledButton = true
    else
      this.isDisabledButton = false
    if (this.nameTextbox.hasError('required')) {
      this.errorMessage = 'カメラ名称を入力してください。';
      this.isDisabledButton = true;
      return
    }
  }
  checkValues(): void {
  if (this.name == this.nameTextbox.value && this.isMasking == this.initIsMasking)
      this.isDisabledButton = true
    else
      this.isDisabledButton = false
  }
}
