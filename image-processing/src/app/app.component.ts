import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common'
import { MatRadioModule } from '@angular/material/radio';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatToolbar} from '@angular/material/toolbar'
import { CdkListbox, CdkOption } from '@angular/cdk/listbox';
import { MatTableModule } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatDialog } from '@angular/material/dialog'
import * as Components  from './component';
import * as Services from './service/';
import { ModelType } from './constant/';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    FormsModule,
    ReactiveFormsModule,
    CommonModule,
    MatRadioModule, 
    MatButtonModule,
    MatIconModule,
    MatInputModule,
    MatFormFieldModule,
    MatToolbar,
    CdkListbox, 
    CdkOption,
    MatTableModule,
    MatPaginator,
    ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})

export class AppComponent implements OnInit {
  protected selectedModel: string = ModelType.DETECTION.toString();
  protected displayedColumns: string[] = ['position', 'name', 'weight'];
  constructor(public websocket: Services.Websocket, private dialog: MatDialog) {}

  /**
   * コンポーネント初期化時の処理
   */
  public ngOnInit(): void {
    this.websocket.initialize();

    document.addEventListener('DOMContentLoaded', () => {
      this.doLoad();
    });
  }

  /**
   * ページロード時の処理
   */
  private doLoad(): void {
    this.websocket.pageLoad();
  }

  /**
   * カメラ登録
   */
  openRegistCameraDialog(): void {
    const dialogRef = this.dialog.open(Components.Dialogs.RegistCamera, {
      data: {
        websocket: this.websocket,
      }
    });

    dialogRef.afterClosed().subscribe(result =>{
      console.log('Close regist camera dialog')
    })
  }

  /**
   * 画像表示ダイアログ表示処理
   * @param {number} id カメラID
   * @param {string} name 名称
   * @param {boolean} isMasking マスキングフラグ
   */
  openImageViewDialog(id: number , name: string, isMasking: boolean, isWebsocket: boolean): void {
    const dialogRef = this.dialog.open(Components.Dialogs.ImageView, {
      data: {
        websocket: this.websocket,
        id: id,
        name: name,
        isMasking: isMasking,
        isWebsocket: isWebsocket,
      }
    })

    // ダイアログが閉じられたときの処理
    dialogRef.afterClosed().subscribe(result =>{
      console.log('Close image view dialog')
    })
  }

  /**
   * カメラ設定ダイアログ表示
   * @param {number} id カメラID
   * @param {string} name 名称
   * @param {boolean} isMasking マスキングフラグ
   */
  openSettingCameraDialog(id: number , name: string, isMasking: boolean): void {
    const dialogRef = this.dialog.open(Components.Dialogs.ChangeSettingCamera, {
      data: {
        websocket: this.websocket,
        id: id,
        name: name,
        isMasking: isMasking,
      }
    });

    // ダイアログが閉じられたときの処理
    dialogRef.afterClosed().subscribe(result =>{
      console.log('Close setting camera dialog')
    })
  }

  /**
   * カメラ解除ダイアログ表示
   * @param {number} id カメラID
   */
  openUnsubscribeCameraDialog(id: number): void {
    const dialogRef = this.dialog.open(Components.Dialogs.UnsubscribeCamera, {
      data: {
        websocket: this.websocket,
        id: id,
      }
    });

    // ダイアログが閉じられたときの処理
    dialogRef.afterClosed().subscribe(result =>{
      console.log('Close unsubscraibe camera dialog')
    })
  }
}
