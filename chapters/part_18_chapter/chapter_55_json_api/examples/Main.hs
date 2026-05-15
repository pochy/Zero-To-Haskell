module Main where

data ExternalUser = ExternalUser String
newtype Email = Email String deriving Show

validate :: ExternalUser -> Maybe Email
validate (ExternalUser value)
  | '@' `elem` value = Just (Email value)
  | otherwise = Nothing

main :: IO ()
main = print (validate (ExternalUser "a@example.com"))
