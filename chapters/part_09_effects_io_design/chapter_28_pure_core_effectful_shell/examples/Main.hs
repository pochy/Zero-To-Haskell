module Main where

normalize :: String -> String
normalize = unwords . words

main :: IO ()
main = do
  let raw = "  Haskell   Tutorial  "
  putStrLn (normalize raw)
