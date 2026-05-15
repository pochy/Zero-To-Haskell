{-# LANGUAGE BangPatterns #-}
module Main where

strictSum :: [Int] -> Int
strictSum = go 0
  where
    go !acc [] = acc
    go !acc (x:xs) = go (acc + x) xs

main :: IO ()
main = print (strictSum [1..100])
