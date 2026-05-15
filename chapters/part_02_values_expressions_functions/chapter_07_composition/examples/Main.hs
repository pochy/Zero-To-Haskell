module Main where

process :: [Int] -> Int
process = sum . map (* 2) . filter (> 0)

main :: IO ()
main = print (process [-1, 2, 3])
