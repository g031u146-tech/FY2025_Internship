import cv2

class MotionDetect():
    def __init__(self):
        self.before = None

    # 変化箇所に枠線を描画 #
    def detection(self, frame):
        # 枠線の色
        box_color = (0, 0, 255)   
        
        # 白黒画像に変換
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self.before is None:
            self.before = gray.astype("float")
            return None

        # 現在のフレームと移動平均との差を計算
        cv2.accumulateWeighted(gray, self.before, 0.6)
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(self.before))

        # frameDeltaの画像を2値化
        thresh = cv2.threshold(frameDelta, 3, 255, cv2.THRESH_BINARY)[1]
        
        # 輪郭のデータを得る
        contours = cv2.findContours(thresh,
                        cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)[0]
        
        # 差分があった点を画面に描く
        for target in contours:
            x, y, w, h = cv2.boundingRect(target)
            if w < 50: continue # 小さな変更点は無視
            cv2.rectangle(frame, (x, y), (x+w, y+h), box_color, 2)
        
        return(frame)