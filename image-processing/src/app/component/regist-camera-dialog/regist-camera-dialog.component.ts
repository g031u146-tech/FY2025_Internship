import { Component, Inject, AfterViewInit } from '@angular/core';
import { FormsModule, } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogRef, MatDialogContent, MatDialogActions, MatDialogTitle, MatDialogClose, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatInputModule } from '@angular/material/input';
import { MatPaginator } from '@angular/material/paginator';
import { MatIconModule } from '@angular/material/icon';
import * as Interfaces from '../../interface';

@Component({
  selector: 'app-regist-camera-dialog',
  standalone: true,
  imports: [
    FormsModule,
    MatButtonModule,
    MatTableModule,
    MatPaginator,
    MatDialogTitle, MatDialogContent, MatDialogActions, MatDialogClose,
    MatInputModule,
    MatIconModule,
  ],
  templateUrl: './regist-camera-dialog.component.html',
  styleUrl: './regist-camera-dialog.component.scss'
})
export class RegistCameraDialogComponent  {
  protected displayedColumns: string[] = ['hostname', 'ipAddress'];
  protected clickRowData: Interfaces.UnregisteredCameraInfo | undefined = undefined;
  public name: string = '';

  /**
   * コンストラクタ
   * @param dialogRef ダイアログ参照
   * @param data ダイアログデータ
   */
  constructor (private dialogRef: MatDialogRef<RegistCameraDialogComponent>, @Inject(MAT_DIALOG_DATA) public data: any) {}

  /**
   * 行クリックイベント
   * @param row 行データ
   */
  onClickRow(row: any): void {
    // 同じ行をクリックしたら解除
    this.clickRowData = this.clickRowData == row ? undefined : row;
  }

  /**
   * 登録ボタンイベント
   */
  onRegist(): void {
  }

  /**
   * 閉じるボタンイベント
   */
  onClose(): void {
    this.dialogRef.close();
  }
}
