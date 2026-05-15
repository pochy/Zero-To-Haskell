module Main where

data Option a = None | Some a deriving Show

main :: IO ()
main = print (Some "TypeScriptでも似た抽象を作れる")
