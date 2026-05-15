module Main where

safeLast :: [a] -> Maybe a
safeLast [] = Nothing
safeLast xs = Just (last xs)

main :: IO ()
main = print (safeLast [1,2,3])
