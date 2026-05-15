module Main where

newtype Config = Config { greeting :: String }

greet :: Config -> String -> String
greet config name = greeting config ++ ", " ++ name

main :: IO ()
main = putStrLn (greet (Config "Hello") "Ada")
