module Main where

findUser :: Int -> Maybe String
findUser 1 = Just "Ada"
findUser _ = Nothing

orders :: String -> Maybe [String]
orders name = Just [name ++ "-order"]

main :: IO ()
main = print (findUser 1 >>= orders)
