# Capstone Project: 型安全なタスク処理アプリ

このプロジェクトは、チュートリアル全体の考え方を小さな実務アプリにまとめる最終演習です。目的は機能の多さではなく、型、純粋性、副作用、エラー、テストの境界を説明できることです。

## 実行

```bash
docker-compose run --rm tutorial cabal run capstone
docker-compose run --rm tutorial cabal test all
```

期待する出力:

```text
#1 [high] Write tutorial review
```

## 設計

- `TaskInput` は外部入力を検証した後の値です。
- `Task` はアプリ内部で扱うドメイン値です。
- `AppError` は失敗理由を文字列ではなく型として表します。
- `runWorkflow` は Pure Core なので、`IO` なしでテストできます。
- `app/Main.hs` は Effectful Shell として、結果の表示だけを担当します。

## レビュー課題

```text
1. `String` のまま扱っている値を、さらに `newtype` に分けるならどこか。
2. `AppError` を利用者向けメッセージへ変換する境界はどこに置くべきか。
3. JSONやDBを追加する場合、外部表現と内部モデルをどこで変換するか。
4. ログ、設定、テストを追加してもPure Coreを保てるか。
```
