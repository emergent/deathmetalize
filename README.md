# Deathmetalizer

## これは何？

技術書典7で頒布予定の[機械学習の炊いたん2](https://tomo-makes.booth.pm/items/1573331)に掲載の「作って遊ぼうデスメタル」内で解説しているプログラムのソースコード等を格納するリポジトリです。

## dmize.py

歌声をデスヴォイスに変換するプログラムです。

## Wave-U-Netについて

本編では、[Wave-U-Net](https://github.com/f90/Wave-U-Net)について触れており、その中で執筆時点での`tensorflow`バージョン（1.14.0）で実行するため、[オリジナルのコード](https://github.com/f90/Wave-U-Net/commit/f359d27beb10a9ef27022714b8a4d8157ac6650d)に手をいれています。

`patch`ディレクトリの中に、修正した内容を適用するパッチを格納していますので、お使いください。
