# testcase-generator

![verification status](https://github.com/naskya/testcase-generator/actions/workflows/verify.yml/badge.svg)

競技プログラミングの問題のテストケースを生成したり、生成したケースでテストを行って不正解となるケースや実行時エラーが発生するケースを探索したりするためのツールです。

https://user-images.githubusercontent.com/48414671/191260539-6be4e6d3-334a-48cb-bdb3-7e2861795819.mp4

- 整数・浮動小数点数
- 文字列
- 整数・浮動小数点数の配列
- 文字列の配列
- 整数・浮動小数点数の行列
- グラフ (以下の設定が可能)
    - 頂点数
    - 辺数
    - 辺に重み有り / 辺に重み無し
    - 多重辺無し / 多重辺無しとは限らない
    - 自己ループ無し / 自己ループ無しとは限らない
    - 閉路無し / 閉路無しとは限らない
    - 連結 / 連結とは限らない
    - 有向 / 無向

を生成することができます。

主に競技プログラミングのコンテスト中にデバッグの目的で使用することを想定しているため汎用的であること・少ない労力で簡単にテストの生成ができること・小さいテストケースを高速かつ大量に生成，テストできることを重視しています。

一方で、作問をした人が問題のためにテストケースを用意するために用いる場合や大きいテストケースや特殊なテストケースを生成する場合などには適していない可能性があります。

# 使い方

使用には [Python 3.9](https://www.python.org/downloads/) (またはそれ以上)と、[requirements.txt](https://github.com/naskya/testcase-generator/blob/main/requirements.txt) に記載されているライブラリのインストールが必要です。[pip](https://pip.pypa.io/en/stable/) を使用する場合、以下のコマンドで必要なライブラリをインストールできます。

```bash
$ pip3 install -r requirements.txt
```

このツールは、生成するテストケースを指定するテキストファイルを作成してコマンドライン引数として与えて使用します。

例えば

```
int A [1, 100]
int B [1, 1000]
---
A B
```

というテキストファイルを `in.txt` という名前で作成して

```bash
$ ./main.py gen -i in.txt -c 100
```

などとすると、1 以上 100 以下の整数と 1 以上 1000 以下の整数が空白区切りで並んだテストケースが 100 個生成されます。

詳細な説明は以下の通りです。

- [生成するテストケースを指定するテキストファイルを作成する](https://github.com/naskya/testcase-generator/blob/main/docs/input.md) (この説明は下記の使用例に少し目を通してから読んだ方が分かりやすいと思います。)
- [テストケースの生成を行う](https://github.com/naskya/testcase-generator/blob/main/docs/gen.md)
- [テストケースを生成してテストを実行する](https://github.com/naskya/testcase-generator/blob/main/docs/test.md)

# インストール

個人的に使用するツールとして作ったため、特にパッケージマネージャへの登録などは行っていません(需要があれば考えます)。このリポジトリを好きな場所にクローンして、エイリアスなどを作成してお使いください。例えば Linux で bash をお使いなら、

```bash
$ git clone https://github.com/naskya/testcase-generator.git
$ cd testcase-generator
$ echo "alias testcase-generator=\"python3 `pwd -P`/main.py\"" >> ~/.bashrc
```

などとエイリアスを作成すると

```bash
$ testcase-generator gen -i in.txt -c 100
```

という風に `testcase-generator` コマンドを使えるようになります。

# 使用例

[`samples` ディレクトリ](https://github.com/naskya/testcase-generator/tree/main/samples)に AtCoder の問題のテストケースを生成するコードが入っています。ただし、数列の長さの範囲などは元の問題の制約よりも大幅に小さくなっています(`N` ≤ 10⁵ → `N` ≤ 100 など)。これはテストケースの種類によっては大きなものを生成するのに時間が掛かる場合があるから、また撃墜ケースが見つけられても大きいテストケースだとどこにバグが有るのか探すのが困難なことがよくあるからです。実際にコンテスト中に使用する際もこのように小さいテストケースを生成するために使うことをおすすめします。

# バグ報告など

バグ報告は [Issues](https://github.com/naskya/testcase-generator/issues) へお願いします。疑問点があれば [Discussions](https://github.com/naskya/testcase-generator/discussions) に Q&A のスレッドを立ててください。
