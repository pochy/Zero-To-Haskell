module Main where

data User = Guest | Registered String deriving Show

describe :: User -> String
describe Guest = "guest"
describe (Registered email) = "registered: " ++ email

main :: IO ()
main = putStrLn (describe (Registered "a@example.com"))
