module Main where

data Route = GetUser Int | Health

describe :: Route -> String
describe Health = "GET /health"
describe (GetUser n) = "GET /users/" ++ show n

main :: IO ()
main = putStrLn (describe (GetUser 42))
