module Main where

parsePositive :: Int -> Either String Int
parsePositive n
  | n > 0 = Right n
  | otherwise = Left "positive number required"

main :: IO ()
main = print (parsePositive 3)
