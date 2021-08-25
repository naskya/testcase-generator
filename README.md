# testcase-generator

競技プログラミングの問題のテストケースを生成したり、生成したケースでテストを行って不正解となるケースや実行時エラーが発生するケースを探索したりするためのツールです。

https://user-images.githubusercontent.com/48414671/130788037-33f81975-6d5b-415b-9f16-7bd8056c464b.mp4

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

主に競技プログラミングのコンテスト中にデバッグの目的で使用することを想定しているため汎用性や早くテストの生成コードが書けることを重視しています。そのため、あまり大きなケースを生成するのには向いていません。

[Python 3.9](https://www.python.org/downloads/) (またはそれ以上), [colorama](https://pypi.org/project/colorama/), [psutil](https://pypi.org/project/psutil/) のインストールが必要です。

# 使い方

[テストケースの生成のみを行う](https://github.com/naskya/testcase-generator/blob/main/docs/gen.md)

[テストケースを生成してテストを実行する](https://github.com/naskya/testcase-generator/blob/main/docs/test.md)

# 使用例

[`samples` ディレクトリ](https://github.com/naskya/testcase-generator/tree/main/samples)に AtCoder の問題のテストケースを生成するコードが入っています。使い方の説明にある通り、

```bash
$ ./main.py gen -i samples/abc215/a.txt
```

などとするとテストケースが生成されます。
