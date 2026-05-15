# START HERE

## 今日やること

1. DockerまたはGHCupでHaskellを実行できる状態にする。
2. 第0章で思想を読む。
3. 第1章の `Hello, World!` を実行する。
4. 第2章でGHCiの `:t` を使い、型を見る習慣を作る。

## Dockerで始める

ローカル環境を汚したくない場合はDockerで進めます。

```bash
docker-compose build tutorial
docker-compose run --rm tutorial cabal build all
docker-compose run --rm tutorial runghc chapters/part_01_hello_world/chapter_01_hello_world/examples/Main.hs
docker-compose run --rm tutorial ghci
```

コンテナ内で章を進める場合:

```bash
docker-compose run --rm tutorial bash
cd chapters/part_01_hello_world/chapter_01_hello_world
runghc examples/Main.hs
```

## GHCupで始める

公式にはGHCupを使う方法が推奨されています。

```bash
curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh
ghcup tui
ghc --version
cabal --version
```

VS Code、Neovim、Emacsなどを使う場合は Haskell Language Server も入れてください。

## 各章の使い方

```text
README.md を読む
examples/Main.hs を読む
runghc examples/Main.hs で動かす
exercises.md を解く
進級チェックに答える
公式docsを確認する
```

## 学習時間の目安

```text
第0部から第5部: 1日30-60分で2-3週間
第6部から第12部: 1日60分で3-5週間
第13部から第18部: 小さなアプリを作りながら4-8週間
第19部から第22部: 必要な章を選び、総合演習で確認
```

## つまずいたとき

- 型エラーは敵ではなく、設計のフィードバックです。
- `IO` が出てきたら、副作用の境界を探してください。
- `Maybe` や `Either` が出てきたら、失敗可能性が型に出ていると考えてください。
- 分からない抽象は、まず具体型 `Maybe`、`[]`、`Either String` で試してください。
