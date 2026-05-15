module Main where

data DbUser = DbUser Int String
data User = User String deriving Show

toDomain :: DbUser -> Either String User
toDomain (DbUser _ email)
  | '@' `elem` email = Right (User email)
  | otherwise = Left "invalid email in database"

main :: IO ()
main = print (toDomain (DbUser 1 "a@example.com"))
