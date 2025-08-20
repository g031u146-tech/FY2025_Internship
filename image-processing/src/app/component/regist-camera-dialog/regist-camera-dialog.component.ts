import { Component, Inject, AfterViewInit } from '@angular/core';
import { FormsModule, FormControl, ReactiveFormsModule, Validators} from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogRef, MatDialogContent, MatDialogActions, MatDialogTitle, MatDialogClose, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatInputModule } from '@angular/material/input';
import { MatPaginator } from '@angular/material/paginator';
import { MatIconModule } from '@angular/material/icon';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import * as Interfaces from '../../interface';
import {merge} from "rxjs";
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { TransmissionType } from '../../constant';
@Component({
  selector: 'app-regist-camera-dialog',
  standalone: true,
  imports: [
    FormsModule, ReactiveFormsModule, 
    MatButtonModule,
    MatTableModule,
    MatPaginator,
    MatDialogTitle, MatDialogContent, MatDialogActions, MatDialogClose,
    MatInputModule,
    MatIconModule,
    MatSlideToggleModule
  ],
  templateUrl: './regist-camera-dialog.component.html',
  styleUrl: './regist-camera-dialog.component.scss'
})
export class RegistCameraDialogComponent  {
  protected displayedColumns: string[] = ['hostname', 'ipAddress'];
  protected clickRowData: Interfaces.UnregisteredCameraInfo | undefined = undefined;
  public name: string = '';
  public isMasking: boolean = true

  public errorMessage: string = '';

  public isFormDisabled: boolean = true;
  public isButtonDisabled: boolean = true;
  public nameTextbox = new FormControl('', [Validators.required, Validators.maxLength(20)])

  
  

  /**
   * コンストラクタ
   * @param dialogRef ダイアログ参照
   * @param data ダイアログデータ
   */
  constructor (private dialogRef: MatDialogRef<RegistCameraDialogComponent>, @Inject(MAT_DIALOG_DATA) public data: any) {
    merge(this.nameTextbox.statusChanges, this.nameTextbox.valueChanges)
    .pipe(takeUntilDestroyed())
    .subscribe(()=>this.updateErrorMessage())

    this.isFormDisabled = true;
    this.nameTextbox.setValue('')
    this.nameTextbox.disable();
    this.isButtonDisabled = true

  }

  /**
   * 行クリックイベント
   * @param row 行データ
   */
  onClickRow(row: any): void {
    // 同じ行をクリックしたら解除
    this.clickRowData = this.clickRowData == row ? undefined : row;

    this.isFormDisabled = this.clickRowData == undefined;
    if (this.clickRowData) {
      this.nameTextbox.enable();
    }
    else {
      this.nameTextbox.setValue('')
      this.nameTextbox.disable()
      this.isButtonDisabled = true
    }
  }

  updateErrorMessage(): void{
    this.errorMessage = '';

    if (this.nameTextbox.hasError('required')){
      this.errorMessage = "カメラ名称を入力してください。"
      this.isButtonDisabled = true
      return
    }

    this.isButtonDisabled = false
  }
  /**
   * 登録ボタンイベント
   */
  onRegist(): void {
    this.data.websocket.dialogRef = this.dialogRef
    this.data.websocket.textbox = this.nameTextbox
    this.nameTextbox.disable()


    this.data.websocket.Subject$.next(JSON.stringify({
      'transmissionType': TransmissionType.CAMERA_REGISTERATION,
      'data': {
        'hostname': this.clickRowData?.hostname,
        'ipAddress': this.clickRowData?.ipAddress,
        'name': this.nameTextbox.value,
        'isMasking': this.isMasking
      }
    }))
  }

  /**
   * 閉じるボタンイベント
   */
  onClose(): void {
    if (this.clickRowData) {
      if (!this.nameTextbox.invalid) {
        if (!confirm('このまま終了しますか？')) return
      }
    }
      

    this.dialogRef.close();
  }
}
