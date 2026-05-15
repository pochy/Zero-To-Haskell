module Main where

data RegistrationError = EmptyEmail | ShortPassword deriving Show

register :: String -> String -> Either RegistrationError String
register "" _ = Left EmptyEmail
register _ password | length password < 8 = Left ShortPassword
register email _ = Right email

main :: IO ()
main = print (register "ada@example.com" "secret")
