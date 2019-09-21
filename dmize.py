import numpy as np
from scipy.io.wavfile import read, write
import sys
import matplotlib.pyplot as plt

args = sys.argv
if len(args) < 2:
    print('specify input wav file.')
    exit

# 入力ファイルの読み込み
wavfile = args[1]
fs, data = read(wavfile)


# フーリエ変換のための準備
# 実装は以下サイトのコードを参照した。
# https://qiita.com/namaozi/items/dec1575cd455c746f597
nfft = 1024
overlap = nfft // 2  # オーバーラップする範囲
frame_length = data.shape[0]

time_song = float(frame_length) / fs
time_unit = 1.0 / float(fs)

start = (nfft // 2) * time_unit
stop = time_song
step = (nfft - overlap) * time_unit
time_ruler = np.arange(start, stop, step)

window = np.hamming(nfft)
spec = np.zeros([len(time_ruler), int(nfft)], dtype=np.complex)
pos = 0


# フーリエ変換の実行
for fft_index in range(len(time_ruler)):
    frame = data[pos:pos+nfft]
    if len(frame) == nfft:
        #windowed = window * frame
        windowed = frame  # 窓関数をかけると書き戻し時に変になるのでかけないことにした
        fft_result = np.fft.fft(windowed)
        # print(len(windowed), len(fft_result))
        for i in range(len(spec[fft_index])):
            # spec[fft_index][-i-1] = fft_result[i]
            # print(spec[fft_index])
            # print(fft_result[i])
            spec[fft_index][i] = fft_result[i]

        pos += int(nfft - overlap)


# 周波数成分の操作
# スペクトルの値を1/2の周波数成分に移動するだけの簡単なもの

'''
for i in range(len(spec)):
    l = len(spec[i])
    for j in range(l//2):
        spec[i][j] = spec[i][-1-j]
'''

N = 200
x = np.arange(0, fs, fs/len(spec[N]))
y = np.abs(spec[N])
plt.plot(x, y)
# plt.show()

for i in range(len(spec)):
    l = len(spec[i])
    for j in range(l//2):
        # 意味があるのかよくわからない係数
        # より低域のスペクトル値を強調するためにかけている
        # 大きすぎるとwavに戻した時にクリップしてしまうので控えめに
        coef = 1+(l-j)*0.001

        if j*2 < l/2:
            spec[i][j] = spec[i][j*2] * coef
            spec[i][-2-j] = spec[i][-2-j*2] * coef
        else:
            spec[i][j] = 0+0j
            spec[i][-2-j] = 0+0j

N = 200
x = np.arange(0, fs, fs/len(spec[N]))
y = np.abs(spec[N])
plt.plot(x, y)
# plt.show()


# 逆フーリエ変換（IFFT）をかけてwavファイルを書き出す

wavout = wavfile[:-4]+'_2.wav'
outdata = np.zeros(len(data), dtype=np.int16)
for ifft_index in range(len(spec)):
    ifft_result = np.fft.ifft(spec[ifft_index])
    ifft_result = ifft_result.real

    for i, r in enumerate(ifft_result):
        pos = ifft_index * int(nfft-overlap)+i
        if pos < len(data):
            outdata[pos] = int(r)

write(wavout, fs, outdata)
