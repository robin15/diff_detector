# Opencvでmp4ファイルをオープンして、初めに一フレーム目の画像を表示して、
# 1つ以上の領域をマウスドラッグによる選択を受け付けて領域情報を保持した後に、
# ループ処理にて、各フレームをグレースケーリング処理した後に二値化し、
# 先ほど選択した各領域についてn+1枚目のフレームとn枚目のフレームの画像差分値が
# 所定値以上であるときに、その時のループ回数を標準出力へ出力するpythonコードは？

import cv2

# 初めに一フレーム目を表示し、領域を選択
cap = cv2.VideoCapture('sample.mp4')
ret, frame = cap.read()
# cv2.imshow('frame', frame)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
roi = cv2.selectROI(frame)

print(roi)
# 二値化のためのしきい値
threshold_value = 50

# 前のフレームを保存するための変数
previous_frame = None

# ループ回数をカウントする変数
loop_count = 0

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        # グレースケール変換
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 領域のみに切り抜き
        roi_gray = gray[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
        
        # 二値化
        roi_bin, thresh = cv2.threshold(roi_gray, threshold_value, 255, cv2.THRESH_BINARY)
        
        # 差分を計算
        if previous_frame is not None:
            diff = cv2.absdiff(thresh, previous_frame)
            # 差分の合計を計算
            diff_sum = diff.sum()
            cv2.imshow('roi_bin', diff)
            
            # 差分が所定値以上である場合にループ回数を出力
            if diff_sum > threshold_value:
                print("loop count:", loop_count)
        
        # 前のフレームを保存
        previous_frame = thresh
        
        # ループ回数をカウント
        loop_count += 1
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# 終了処理
cap.release()
cv2.destroyAllWindows()
