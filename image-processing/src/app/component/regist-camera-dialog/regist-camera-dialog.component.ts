import { Component, Inject, ViewChild, AfterViewInit } from '@angular/core';
import { Subject } from "rxjs";
import { FormsModule, } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogRef, MatDialogContent, MatDialogActions, MatDialogTitle, MatDialogClose, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatInputModule } from '@angular/material/input';
import { MatPaginator } from '@angular/material/paginator';
import { MatIconModule } from '@angular/material/icon';
import { UnregisteredCameraInfoInterface } from '../../interface/unregistered-camera-info.interface';

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
export class RegistCameraDialogComponent implements AfterViewInit  {
  private subject$: Subject<string> = new Subject<string>();

  protected displayedColumns: string[] = ['hostname', 'ipAddress'];
  protected clickRowData:UnregisteredCameraInfoInterface | undefined = undefined;

  public dataSource = new MatTableDataSource<UnregisteredCameraInfoInterface>([]);

  public name: string = '';

  @ViewChild('paginator') paginator!: MatPaginator;
  
  constructor (private dialogRef: MatDialogRef<RegistCameraDialogComponent>, @Inject(MAT_DIALOG_DATA) private data: any) {
    // 未登録カメラ一覧情報要求
    let tmpDataSource: {
      hostname: string;
      ipAddress: string;
    }[] = [];

    this.data.jsonData["cameraInfo"].forEach((element: any) => {
      tmpDataSource.push({
        'hostname': element['hostname'],
        'ipAddress': element['address']  
      })
    });

    this.subject$ = this.data.subject;
    this.dataSource = new MatTableDataSource(tmpDataSource); 
  }

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
  }

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
    if (!this.clickRowData) {
      alert("登録するカメラを選択してください")
      return
    }
    if (!this.name) {
      alert("カメラ名を")
    }

    // カメラ登要求
    this.subject$.next(JSON.stringify({
      'transmissionType': 0x20,
      'cameraIp': this.clickRowData?.ipAddress,
      'cameraName': this.name,
      'maskingFlag': true
    }))

    this.dialogRef.close();
  }

  disabledRegistButton(): boolean {
    return this.clickRowData == undefined || this.name == ''
  } 

  /**
   * 閉じるボタンイベント
   */
  onClose(): void {
    this.dialogRef.close();
  }
}
