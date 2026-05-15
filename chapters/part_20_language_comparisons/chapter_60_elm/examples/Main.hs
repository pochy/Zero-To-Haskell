module Main where

data Msg = Increment | Decrement

update :: Msg -> Int -> Int
update Increment n = n + 1
update Decrement n = n - 1

main :: IO ()
main = print (update Increment 41)
