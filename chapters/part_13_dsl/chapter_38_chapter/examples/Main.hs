module Main where

parseDigit :: Char -> Maybe Int
parseDigit c
  | c >= '0' && c <= '9' = Just (fromEnum c - fromEnum '0')
  | otherwise = Nothing

main :: IO ()
main = print (parseDigit '7')
