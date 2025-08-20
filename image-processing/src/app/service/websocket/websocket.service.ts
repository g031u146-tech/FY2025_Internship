import { Injectable, ViewChild } from '@angular/core';
import { Subject } from 'rxjs';
import { webSocket } from "rxjs/webSocket";
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator'
import { TransmissionType, ClientType, ModelType } from '../../constant';
import * as Models from '../../model/';

@Injectable({
  providedIn: 'root'
})


/**
 * Websocketサービスクラス
 */
export class WebsocketService {
  //#region constants
  /**
   * 接続先サーバのホスト名
   * @type {string}
   * @private
   * @
   */
  private readonly HOST: string = 'localhost';
  /**
   * 接続先サーバのポート番号
   * @type {number}
   * @private
   */
  private readonly PORT: number = 54321;
  //#endregion
  //#region Properties
  /**
   * WebSocketのSubject
   * @type {Subject<string>}
   * @public
   */
  public Subject$: Subject<string> = new Subject<string>();
  /**
   * 画像データ
   * @type {any}
   * @public
   */
  public ImageData: any;
  /**
   * WebSocketの接続状態
   * @type {boolean}
   * @public
   */
  public isConnected: boolean = false;
  /**
   * WebSocketの接続完了状態
   * @type {boolean}
   * @public
   */
  public isComplete: boolean = false;
  /**
   * 登録済みカメラリデータソース
   * @type {MatTableDataSource<Models.RegistedCameraInfo>}
   * @public
   */
  public registedCameraDataSource: MatTableDataSource<Models.RegistedCameraInfo> = new MatTableDataSource<Models.RegistedCameraInfo>([]);
  /**
   * 接続済みカメラリデータソース
   * @type {MatTableDataSource<any>}
   * @public
   */
  public connectedCameraDataSource: MatTableDataSource<any> = new MatTableDataSource<any>([]);
  /**
    * 選択されたカメラ
    * @type {string | undefined}
    * @public
    */
  public selectCamera: string | undefined= undefined;
  /**
   * キャンバス要素
   * @type {any}
   * @public
   */
  public canvas: any;
  /**
   * キャンバスのコンテキスト
   * @type {any}
   * @public
   */
  public context: any;

  @ViewChild('paginator') public registedCameraPaginator!: MatPaginator;
  @ViewChild('paginator') public connectedCameraPaginator!: MatPaginator;
  
  //#endregion

  /**
   * 受信データ
   * @type {string}
   * @private
   */
  private receiveData: string = '';

  /**
   * コンストラクタ
   */
  constructor() { }

  /**
   * 初期化処理
   */
  public initialize(): void {
    this.isConnected = false;
    this.isComplete = false;
    this.registedCameraDataSource.paginator = this.registedCameraPaginator;
    this.connectedCameraDataSource.paginator = this.connectedCameraPaginator;
    this.websocketOperaion();
  }

  /**
   * ページロード時の処理
   */
  public pageLoad(): void {
    this.canvas = document.getElementById("canvas") as HTMLCanvasElement;
    this.context = this.canvas.getContext('2d');
    this.canvas.width = 320;
    this.canvas.height = 240;

    // websocketのタイマー処理を開始
    this.timerCallback();
  }

  /**
   * WebSocketの接続を操作
   */
  private websocketOperaion(): void {
    // WebSocketが接続されている場合
    if (this.isConnected) {
      this.isComplete = true;
      this.registedCameraDataSource = new MatTableDataSource<Models.RegistedCameraInfo>([]);
      this.connectedCameraDataSource = new MatTableDataSource<any>([]);
      this.selectCamera = undefined;
      this.Subject$.complete();
      return;
    }

    this.Subject$ = this.connect()

    this.Subject$.subscribe(
      msg => {
        let jsonData = JSON.parse(msg)
        console.log(jsonData)

        switch (jsonData['transmissionType']) {
          // 伝送種別が「接続」の場合
          case TransmissionType.CONECT:
            this.transmissionConnect(jsonData);
            break;
          // 伝送種別が「ストリーミング」の場合
          case TransmissionType.STREAMING:
            this.transmissionStreaming(jsonData);
            break;
          // 伝送種別が「表示カメラ切替要求」の場合
          case TransmissionType.CHENGE_VIEW_CAMERA:
            //this.transmissionChangeViewCamera(jsonData);
            break;
          // 伝送種別が「カメラ接続情報要求」の場合
          case TransmissionType.CAMERA_CONNECTED_INFO:
            this.transmissionCameraConnectedInfo(jsonData);
            break;
          // 伝送種別が「カメラ登録情報要求」の場合
          case TransmissionType.CAMERA_REGISTED_INFO:
            this.transmissionCameraRegistedInfo(jsonData);
            break;
          // 伝送種別が「カメラ登録要求」の場合
          case TransmissionType.CAMERA_REGISTERATION:
            break;
          // 伝送種別が「カメラ設定変更要求」の場合  
          case TransmissionType.CHANGE_CAMERA_SETTINGS:
             this.transmissionChangeSettingCamera(jsonData);
             break;

          // 伝送種別が「カメラ削除要求」の場合
          case TransmissionType.CAMERA_DELETE:
            this.transmissionCameraDelete (jsonData);
            break;
       

          default:
            console.warn('Unknown transmission type:', jsonData['transmissionType']);
          }
        },
        err => {
          console.warn(err)
          
          if (this.isComplete) {
            console.log('接続を終了しました。')
          } else {
            console.log('サーバとの接続が切れました。')
          }

          this.isConnected = false;
          this.isComplete = false;
        }
      );
  }

  /**
   * WebSocket接続を確立する
   * @returns {Subject<string>} WebSocketのSubject
   */
  private connect(): Subject<string> {
    return webSocket({
      url: `ws://${ this.HOST }:${ this.PORT }`,
      deserializer: ({ data }) => data
    })
  }

  /**
   * 接続要求処理
   * @param jsonData JSONデータ
   * @private
   */
  private transmissionConnect(jsonData: any): void {
    jsonData['message'] = '';
    jsonData['clientType'] = ClientType.VIEWER;
    jsonData['selectCameraId'] = -1;
    jsonData['modelType'] = ModelType.SEGMENTATION;

    this.Subject$.next(JSON.stringify(jsonData))
    this.isConnected = true;
  }

  /**
   * ストリーミング要求処理
   * @param jsonData JSONデータ
   * @private
   */
  private transmissionStreaming(jsonData: any): void {
    this.receiveData += jsonData['data'];
            
    if (jsonData['endPoint']) {
      let imageData = this.receiveData;
      this.receiveData = '';

      let img = new Image();
      let ctx = this.context;
                  
      img.onload = ()=> {
        ctx.drawImage(img, 0, 0)
      }
              
      img.src = 'data:image/png;base64,' + imageData;
      this.ImageData = img.src;
    }
  }

  /**
   * カメラ表示切替要求処理
   * @param jsonData JSONデータ
   * @private
   */
  private transmissionChangeViewCamera(jsonData: any): void {

  }

  /**
   * カメラ接続情報要求処理
   * @param jsonData JSONデータ
   * @private
   */
  private transmissionCameraConnectedInfo(jsonData: any): void {
  }

  /**
   * カメラ登録情報要求処理
   * @param jsonData JSONデータ
   * @private
   */
  private transmissionCameraRegistedInfo(jsonData: any): void {
    this.registedCameraDataSource = new MatTableDataSource<Models.RegistedCameraInfo>([]);
            
    for (let index in jsonData['data']) {    
      let registedCameraInfo = new Models.RegistedCameraInfo();
      registedCameraInfo.jsonToProperty(jsonData['data'][index]);
      
      this.registedCameraDataSource.data.push(registedCameraInfo);
    }
  }

 /**
   * 名称変更
   */

  private transmissionChangeSettingCamera(jsonData: any): void {
    alert(jsonData['result'] ? '変更成功しました。' : '変更失敗しました。')
  }
  

  /**
   *カメラ削除
   */

   private transmissionCameraDelete(jsonData:any):void{
    alert(jsonData['result'] ? ' 削除しました。' : '削除失敗しました。')

}



  /**
   * アラートメッセージ取得
   * @param jsonData JSONデータ
   * @private
   */
  private getAlertMessage(jsonData: any): string {
    switch (jsonData['transmissionType']) {
      case TransmissionType.CAMERA_REGISTERATION:
        return jsonData["result"]  ? "カメラの登録を行いました。" : "カメラの登録が失敗しました。"   
      case TransmissionType.CHANGE_CAMERA_SETTINGS:
        return jsonData["result"] ? "設定変更を行いました。" : "設定変更に失敗しました。" 
     case TransmissionType.CAMERA_DELETE:
        return jsonData["result"] ? "カメラの登録を解除しました。" : "カメラの登録解除に失敗しました。" 
      default:
        return "不明な要求です。";
    }   
  }

  /**
   * タイマー処理
   */
  private timerCallback(): void {
    // 登録済みカメラ情報要求
    this.Subject$.next(JSON.stringify(
      {
        'transmissionType': TransmissionType.CAMERA_REGISTED_INFO
      }
    ));

    // 3秒後に再度タイマー処理を呼び出す
    setTimeout(() => {
      this.timerCallback();
    }, 3000);
  }
}



