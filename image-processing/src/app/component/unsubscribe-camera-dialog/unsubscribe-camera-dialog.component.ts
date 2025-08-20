import { Component, Inject } from '@angular/core';
import { Subject } from "rxjs";
import { MatButtonModule } from '@angular/material/button';
import { MatDialogRef, MatDialogContent, MatDialogActions, MatDialogTitle, MatDialogClose, MAT_DIALOG_DATA } from '@angular/material/dialog';
import * as Services from '../../service/';
import { TransmissionType, } from '../../constant';

@Component({
  selector: 'app-unsubscribe-camera-dialog',
  standalone: true,
  imports: [
    MatButtonModule,
    MatDialogContent, MatDialogActions, MatDialogTitle, MatDialogClose,
  ],
  templateUrl: './unsubscribe-camera-dialog.component.html',
  styleUrl: './unsubscribe-camera-dialog.component.scss'
})
export class UnsubscribeCameraDialogComponent {
  public id = 0

  /**
   * コンストラクタ
   * @param dialogRef 
   * @param data 
   */
  constructor(private dialogRef: MatDialogRef<UnsubscribeCameraDialogComponent>, @Inject(MAT_DIALOG_DATA) private data: any) {
    this.id = data.id
  }

/**
 * 解除ボタンイベント
 */
onConfirm(): void { 
  if( confirm('削除しますか？') ) {
         this.data.websocket.Subject$.next(JSON.stringify(
           {  
                 'transmissionType': TransmissionType.CAMERA_DELETE,
                  'id': this.data.id,
           }
         ));
         return;
     }
}

/**
 * 閉じるボタンイベント
 */
  onClose(): void{
    this.dialogRef.close();
  }
}
