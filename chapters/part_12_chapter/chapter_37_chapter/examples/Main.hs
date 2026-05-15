module Main where

propReverseReverse :: [Int] -> Bool
propReverseReverse xs = reverse (reverse xs) == xs

main :: IO ()
main = print (propReverseReverse [1,2,3])
