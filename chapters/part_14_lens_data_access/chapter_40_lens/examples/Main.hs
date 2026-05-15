module Main where

data User = User { name :: String, age :: Int } deriving Show

birthday :: User -> User
birthday user = user { age = age user + 1 }

main :: IO ()
main = print (birthday (User "Ada" 36))
