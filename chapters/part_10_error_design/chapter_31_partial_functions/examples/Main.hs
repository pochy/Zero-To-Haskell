module Main where

safeHead :: [a] -> Maybe a
safeHead [] = Nothing
safeHead (x:_) = Just x

main :: IO ()
main = print (safeHead ([] :: [Int]))
