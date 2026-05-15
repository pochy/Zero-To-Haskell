module Main where

data Raw
data Verified
newtype Email state = Email String deriving Show

verify :: Email Raw -> Maybe (Email Verified)
verify (Email value)
  | '@' `elem` value = Just (Email value)
  | otherwise = Nothing

main :: IO ()
main = print (verify (Email "a@example.com"))
