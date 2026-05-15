# Checkpoints

このファイルは、23部/71章を Level 0-9 相当の到達段階として確認するための進級表です。章を読んだ量ではなく、設計判断を説明できるかで進みます。

| Level | 対象 | 到達条件 |
| --- | --- | --- |
| 0 Philosophy | 第0部 | Haskellを「手順」ではなく「意味、型、副作用の境界」として説明できる |
| 1 First Touch | 第1部 | DockerでHello Worldを実行し、`main :: IO ()` を説明できる |
| 2 Expressions | 第2部-第5部 | 束縛、関数、ADT、再帰、foldを使い、純粋な変換を書ける |
| 3 Type Design | 第3部-第4部, 第10部 | `newtype`、`Maybe`、`Either` で不正状態と失敗を型に出せる |
| 4 Laziness and Laws | 第6部-第8部 | 遅延評価、型クラス法則、Functor/Applicative/Monadの使い分けを説明できる |
| 5 Effects | 第9部 | Pure Core / Effectful Shellで小さなアプリを分割できる |
| 6 Specification | 第12部 | 例ベーステストと性質ベーステストの役割を分けて使える |
| 7 Integration | 第13部-第18部 | CLI/API/DB/JSON境界で外部表現と内部モデルを分けられる |
| 8 Operations | 第15部-第19部 | 並行性、性能、FFI、再現可能ビルドの運用上のリスクを説明できる |
| 9 Professional | 第20部-第22部 | capstoneを設計、実装、テストし、トレードオフをレビューできる |

## 進級レビューの形式

```text
1. この段階で防げるようになった誤用
2. 型で表した仕様
3. 型では表せないためテストした仕様
4. 副作用の境界
5. 実務で残る運用リスク
```

## Capstone合格条件

```text
□ ドメイン型が `String` や `Int` の裸の値を減らしている
□ 入力検証が `Either AppError a` として表れている
□ Pure Coreを直接テストできる
□ `main` は入出力と表示に近い薄い層になっている
□ エラー、ログ、テスト、ドキュメントの追加方針を説明できる
```
