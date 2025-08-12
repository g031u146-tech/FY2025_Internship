/**
 * 登録済みカメラ情報モデル
 */
export class RegistedCameraInfoModel {
  /** カメラID */
  private _id: number;
  /** ホスト名 */
  private _hostname: string;
  /** 名称 */
  private _name: string;
  /** IPアドレス */
  private _ipAddress: string;
  /** 登録日時 */
  private _registedDate: Date;
  /** マスキングフラグ */
  private _isMasking: boolean;
  /** キャパシティ */
  private _capacity: number;
  /** 検知数 */
  private _count: number;
  /** 割合 */
  private _ratio: number;
  /** 接続タイプ */
  private _connectionType: number; // 0:Websocket, 1:RTSP
  
  /**
   * コンストラクタ
   * @param id カメラID
   * @param hostname ホスト名
   * @param name 名称
   * @param ipAddress IPアドレス
   * @param registedDate 登録日時
   * @param isMasking マスキングフラグ
   * @param capacity キャパシティ
   * @param count 検知数
   * @param ratio 割合
   * @param connectionType 接続タイプ (0:Websocket, 1:RTSP)
   */
  constructor(id: number = -1, hostname: string = '', name: string = '', ipAddress: string = '', registedDate: Date = new Date(), isMasking: boolean = false, capacity: number = 0, count: number = 0, ratio: number = 0, connectionType: number = 0) {
    this._id = id;
    this._hostname = hostname;
    this._name = name;
    this._ipAddress = ipAddress;
    this._isMasking = isMasking;
    this._registedDate = registedDate;
    this._capacity = capacity; 
    this._count = count;
    this._ratio = ratio;
    this._connectionType = connectionType; // 0:Websocket, 1:RTSP
  }

  /** カメラID */
  get id(): number {
    return this._id;
  }
  set id(value: number) {
    this._id = value;
  }
  /** ホスト名 */
  get hostname(): string {
    return this._hostname;
  }
  set hostname(value: string) {
    this._hostname = value;
  }
  /** 名称 */
  get name(): string {
    return this._name;
  }
  set name(value: string) {
    this._name = value;
  }
  /** IPアドレス */
  get ipAddress(): string {
    return this._ipAddress;
  }
  set ipAddress(value: string) {
    this._ipAddress = value;
  }
  /** マスキングフラグ */
  get isMasking(): boolean {
    return this._isMasking;
  }
  set isMasking(value: boolean) {
    this._isMasking = value;
  }
  /** 登録日時 */
  get registedDate(): Date {
    return this._registedDate;
  }
  set registedDate(value: Date) {
    this._registedDate = value;
  }
  /** キャパシティ */
  get capacity(): number {
    return this._capacity;
  }
  set capacity(value: number) {
    this._capacity = value;
  }
  /** 検知数 */
  get count(): number {
    return this._count;
  }
  set count(value: number) {
    this._count = value;
  }
  /** 割合 */
  get ratio(): number {
    return this._ratio;
  }
  set ratio(value: number) {
    this._ratio = value;
  }
  /** 接続タイプ */
  get connectionType(): number {
    return this._connectionType;
  }
  set connectionType(value: number) {
    this._connectionType = value;
  }

  /**
   * JSONデータからプロパティに変換
   * @param jsonData JSONデータ
   */
  public jsonToProperty(jsonData: any): void {
    this.id = jsonData['id'] || -1;
    this.hostname = jsonData['hostname'] || '';
    this.name = jsonData['name'] || '';
    this.ipAddress = jsonData['ipAddress'] || '';
    this.registedDate = new Date(jsonData['registedDate']) || new Date();
    this.isMasking = jsonData['isMasking'] || false;
    this.capacity = jsonData['capacity'] || 0;
    this.count = jsonData['count'] || 0;
    this.ratio = jsonData['ratio'] || 0;
    this.connectionType = jsonData['connectionType'] || 0; // 0:Websocket, 1:RTSP
  }
}