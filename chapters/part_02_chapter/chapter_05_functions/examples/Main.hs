module Main where

add :: Int -> Int -> Int
add x y = x + y

add10 :: Int -> Int
add10 = add 10

main :: IO ()
main = print (add10 5)
