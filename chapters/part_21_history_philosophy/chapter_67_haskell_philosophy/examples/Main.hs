module Main where

decide :: Bool -> String
decide canBePure =
  if canBePure then "純粋関数にする" else "IOの境界に置く"

main :: IO ()
main = putStrLn (decide True)
